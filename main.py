import asyncio
from array import array
from pathlib import Path

import psutil
from faker import Faker
from stario import (
    CompressionConfig,
    Context,
    JsonTracer,
    Relay,
    RichTracer,
    Stario,
    Writer,
    asset,
    at,
    data, 
)
import re



from stario.html import (
    H1,
    H2,
    H3,
    A,
    B,
    Body,
    Div,
    Head,
    Hr,
    Html,
    Img,
    Input,
    Li,
    Link,
    Main,
    Meta,
    P,
    Script,
    Section,
    Source,
    Span,
    Style,
    Tag,
    Title,
    Ul,
    Video,
)
from watchfiles import run_process

# DATABASE

database = {}
NO_PEOPLE = 10
database_x = array("B", [] * NO_PEOPLE)
database_y = array("B", [] * NO_PEOPLE)
database_id = array("B", [] * NO_PEOPLE)
dict_of_user_id_to_slot = {}
port = 2000
# we gon do some ECS

# okay i lied, i need some other stuff as well
main_relay = Relay()
fake = Faker()  # for the debug
refresh_rate = 1 / 30
server_stats = ""

# HTML parts

fragments = {}
fragments["head"] = Head(
    Meta({"charset": "UTF-8"}),
    Meta({"name": "viewport", "content": "width=device-width, initial-scale=1"}),
    Title("cursor party"),
    Link({"rel": "icon", "href": "/static/img/avatar.avif"}),
    Link({"rel": "stylesheet", "href": "/static/css/index.css"}),
    Script(
        {
            "type": "module",
            # 'src': f"/static/js/datastar.js')}"
            "src": "https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.8/bundles/datastar.js",
        }
    ),
    Script(
        {
            "type": "module",
            "src": "/static/js/index.js",
        }
    ),
)

# VIEWS


# a view for the index? really?... i'll fix it later.
# okay fixed.


def parse_user_id(user_id):
    # remove spaces and special characters, avoid conflict with html id
    user_id = re.sub(r"\W+", "", user_id)
    return user_id
# HANDLERS
def build_cursor_div(user_id, pos, main_user_id):
    return Div(
        {
            "class": ["cursor_ai", "gt-s"],
            "style": f"translate: {pos[0]}vw {pos[1]}vh;" if user_id != main_user_id else None,
            "data-main-cursor": user_id == main_user_id,
            "id": parse_user_id(user_id),                    
        },
        Img(
            {
                "src": "/static/img/smol.png",
            }
        ),
        P(user_id),
    )

def build_mouse_trap(main_user_id):
    return Div(
        {"id": "mousetrap"},
        *[
            build_cursor_div(user_id, pos, main_user_id)
            for user_id, pos in database.items()
        ],
    )


async def index(c: Context, w: Writer):
    # user_id = uuid4()
    # bad boy, no user_id until you're grown up
    main_user_id = c.req.cookies.get("user_id")
    if not main_user_id:
        main_user_id = fake.name()
        w.cookie("user_id", main_user_id, httponly=True, secure=False)

    database[main_user_id] = [0, 0]
   
    
    return w.html(
        Html(
            {"lang": "en"},
            fragments["head"],
            data.on("pointermove", "fe_work(evt)"),
            Body(
                {"class": ["gf gc"]},
                { "id": "body" },
                data.on("pointermove", at.post("/mouse"), throttle=refresh_rate),
                Main(
                    {"class": ["gc gt-xxl"]},
                    H1(
                        "Cursor Party",
                        data.ignore_morph(),
                        # on écoute tous les événements (join, leave, move)
                        data.init(at.post("/sync")),
                    ),
                    P({"class": "gt-m"}, "Your name is ", Span(main_user_id)),
                    # P({"class": "gt-s"}, data.json_signals()),
                    P({"id": "server"}, {"class": "gt-s"}, server_stats),
                    P(
                        {"id": "fps", "class": ["gt-s"]}, "FPS: ", int(1 / refresh_rate)
                    ),  # kind of a lie
                    A(
                        {"href": "/settings"},
                        Img(
                            {
                                "id": "wheel",
                                "src": f"/static/{asset('svg/settings.svg')}",
                            },
                        ),
                    ),
                    build_mouse_trap(main_user_id),
                )
            )
        )
    )  # huh? html twice? -> YES SIR.


async def sync(c: Context, w: Writer):
    main_user_id = c.req.cookies.get("user_id")
    
    main_relay.publish("join", main_user_id)
    try:
        async for event,value in w.alive(main_relay.subscribe("*")):
            print("refreshing...",main_user_id, event, value)
            if (event == "join"):
                user_id = value
                if user_id != main_user_id:
                    print(f"adding {user_id}")
                    w.patch(build_cursor_div(user_id,[0,0],main_user_id), selector="#mousetrap", mode="append")
            if (event == "leave"):
                user_id = value
                print(f"removing {user_id}")
                w.remove(f"#{parse_user_id(user_id)}")
            if event == "move":
                user_id, dx,dy = value
                pos = [dx, dy]
                if (user_id != main_user_id):
                    print(f"moving {user_id} to {pos}")
                    w.patch(
                        build_cursor_div(user_id, pos, main_user_id),selector=f"#{parse_user_id(user_id)}"
                    )   
    finally:
        if main_user_id in database:
            del database[main_user_id]
        main_relay.publish("leave", main_user_id)
        print(f"{main_user_id} disconnected", database)


async def mouse(c: Context, w: Writer):
    # careful, data keeps coming when window inactive
    signals = await c.signals()

    dx = signals.get("x")
    dy = signals.get("y")
    
    user_id = c.req.cookies.get("user_id")

    if user_id and user_id in database:
        database[user_id] = [dx, dy]

    main_relay.publish("move", (user_id, dx, dy))
    
    w.empty()


async def settings(c, w):
    # we patch the image... NOOOO wtf am i doing. I need the Tao
    # we send a simple link. but the page is very busy morphing
    return w.html(
        Html(
            fragments["head"],
            Body(
                {
                    "class": ["gf gc"],
                },
                Main(
                    {"id": "main"},
                    Div({"class": "panel"}, "Enter your VIP code"),
                    Input(
                        data.bind("code"),
                    ),
                    Div(
                        {"class": ["button", "gm-m"]},
                        data.on("click", at.post("/code")),
                        "SUBMIT",
                    ),
                    Div(data.json_signals()),
                ),
            ),
        )
    )


async def code(c, w):
    signals = await c.signals()
    code = signals.get("code")
    valid = code in ["lol"]
    if valid:
        w.patch(
            Main(
                {"id": "main"},
                P({"class": "gt-xl"}, "Thanks bossman!"),
                P("redirecting you"),
            )
        )
        await asyncio.sleep(3)
        w.redirect("/")
        # weird.. i don't see it
    else:
        w.redirect("/settings")
        # and here it says not allowed


async def wassup_psutil():
    global server_stats
    while True:
        load_avg = psutil.getloadavg()
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        net = psutil.net_io_counters()
        server_stats = (
            f"Server Status: "
            f"Load Avg (5min) {load_avg[1] * 100:.2f}% | "
            f"Cpu Use {cpu:.2f}% | "
            f"Memory Used {memory.percent:.2f}% of 1.8G | "
            f"Network I/O: Sent {net.bytes_sent / (1024**2):.2f} MB | Recv {net.bytes_recv / (1024**2):.2f} MB"
        )
        await asyncio.sleep(5)


# APP


async def main():
    database.clear()
    asyncio.create_task(wassup_psutil())
    # with RichTracer() as tracer:
    with JsonTracer() as tracer:
        app = Stario(
            tracer,
            
            # compression=CompressionConfig(
            #     # min_size=1024,     # Minimum bytes to compress... what?
            #     # zstd_level=4,  # 1-22 (3 default)
            #     brotli_level=4
            # ),
        )
        app.get("/", index)
        app.post("/mouse", mouse)
        app.get("/settings", settings)
        app.post("/sync", sync)
        app.post("/code", code)

        app.assets("/static", Path(__file__).parent / "static")
        # await app.serve(unix_socket="/run/legovh/tmp.sock")
        await app.serve(port=port)
        


def serve():
    asyncio.run(main())


if __name__ == "__main__":
    # serve()
    run_process(Path(__file__).parent, target=serve)
