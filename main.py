import asyncio
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
    at,
    data,
)
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

# okay i lied, i need some other stuff as well
relay = Relay()  # for the tick
fake = Faker()  # for the debug
refresh_rate = 0.04
server_stats = ""

# VIEWS


def index_init(user_id):
    return Html(
        {"lang": "en"},
        Head(
            Meta({"charset": "UTF-8"}),
            Meta(
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ),
            Title("cursor party"),
            Link({"rel": "icon", "href": "/static/img/avatar.avif')}"}),
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
        ),
        Body(
            {"class": ["gf gc"]},
            data.init(at.get("/index_cqrs")),
        ),
    )


def index_view(user_id):
    # if we want to encapsulate
    # WC_Example = Tag("just-flexin", self_closing=True)
    # WC_Example()
    mousetrap = Div(
        {"id": "mousetrap"},
        *[
            Div(
                {
                    "class": ["cursor_ai", "gt-s"],
                    "style": f"left: {pos[0]}%; top: {pos[1]}%;",
                },
                Img(
                    {
                        "src": "/static/img/smol.png",
                    }
                ),
                P(user_id),
            )
            for user_id, pos in database.items()
        ],
    )
    return Body(
        {"class": ["gf gc"]},
        data.on("pointermove", "$data = fe_work(evt)"),
        Main(
            data.on_interval(
                at.post("/mouse"), duration=f"{int(refresh_rate * 1000)}ms"
            ),
            {"class": ["gc gt-xxl"]},
            H1(
                "Cursor Party",
                data.init("fun()"),
                data.ignore_morph(),
            ),
            P({"class": "gt-m"}, "Your name is ", Span(user_id)),
            # P({'class': "gt-s"}, data.json_signals()),
            P({"id": "server"}, {"class": "gt-s"}, server_stats),
            P(
                {"id": "fps", "class": ["gt-s"]}, "FPS: ", int(1 / refresh_rate)
            ),  # kind of a lie
            mousetrap,
        ),
    )


# HANDLERS


async def index(c: Context, w: Writer):
    # user_id = uuid4()
    # bad boy, no user_id until you're grown up
    user_id = c.req.cookies.get("user_id")
    if not user_id:
        user_id = fake.name()
        w.cookie("user_id", user_id, httponly=True, secure=True)
    # if user_id in db, we here just respawn at 0,0
    # seems like an acceptable behavior
    database[user_id] = [0, 0]
    w.html(index_init(user_id))


async def index_cqrs(c: Context, w: Writer):
    user_id = c.req.cookies.get("user_id")
    if user_id and user_id not in database:
        database[user_id] = [0, 0]
        # okay that was it
    # here, w.alive() ends when the SSE connection disconnects
    async for _ in w.alive(relay.subscribe("refresh")):
        w.patch(index_view(user_id))
        # debug break
        # break
    # maybe that's aggressive... i need to test... yes something wrong
    if user_id and user_id in database:
        del database[user_id]


async def mouse(c: Context, w: Writer):
    # careful, data keeps coming when window inactive
    signals = await c.signals()
    data = signals.get("data")
    if data:
        user_id = c.req.cookies.get("user_id")
        if user_id and user_id in database:
            dx, dy = data
            database[user_id] = [dx, dy]
    w.empty()


# LOOPS


async def refresh(refresh_rate=refresh_rate):
    while True:
        relay.publish("refresh", "")
        await asyncio.sleep(refresh_rate)


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
        await asyncio.sleep(1)


# APP


async def main():
    database.clear()
    asyncio.create_task(refresh())
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
        app.get("/index_cqrs", index_cqrs)
        app.post("/mouse", mouse)

        app.assets("/static", Path(__file__).parent / "static")
        await app.serve(unix_socket="/run/legovh/tmp.sock")
        # await app.serve()


def serve():
    asyncio.run(main())


if __name__ == "__main__":
    # serve()
    run_process(Path(__file__).parent, target=serve)
