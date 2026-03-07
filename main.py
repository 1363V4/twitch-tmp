import json
import asyncio
from pathlib import Path
from uuid import uuid4

from faker import Faker

from watchfiles import run_process

from stario import Context, RichTracer, Stario, Writer, JsonTracer, Relay

from stario import asset, at, data
from stario.html import (
    A,
    B,
    Body,
    Div,
    H1,
    H2,
    H3,
    Head,
    Hr,
    Html,
    Img,
    Li,
    Link,
    Main,
    Meta,
    P,
    Section,
    Script,
    Source,
    Span,
    Style,
    Title,
    Ul,
    Video
)


# DATABASE

database = {}

# okay i lied, i need some other stuff as well
relay = Relay()
fake = Faker()

# VIEWS

def index_init(user_id):
    return Html(
        {"lang": "en"},
        Head(
            Meta({'charset': "UTF-8"}),
            Meta(
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ),
            Title("hello there"),
            Link({
                'rel': "icon",
                'href': f"/static/{asset('img/avatar.avif')}"
            }),
            Link({
                'rel': "stylesheet",
                'href': f"/static/{asset('css/index.css')}"
            }),
            Script({
                'type': "module",
                # 'src': f"/static/{asset('js/datastar.js')}"
                'src': "https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.8/bundles/datastar.js"
            }),
            Script({
                'type': "module",
                'src': f"/static/{asset('js/index.js')}",
            }),
        ),
        Body(
            {'class': ["gf gc"]},
            data.init(at.get("/index_cqrs")),
            data.on('pointermove', "$data = mister(evt)"),
            data.on_interval(at.post("/mouse", request_cancellation="disabled"), duration="30ms"),
            # data.on('click', at.post("/mouse", request_cancellation="disabled")),
            Main(
                {'class': ["gc gt-xxl"]},
                H1("Get in!"),
                Div({'class': "gm-xl"}),
                Section(
                    H2("Stario 2.3.0 released!!!"),
                    P({'class': "gt-s"}, "We're getting Comment tags wouhouuuu"),
                    P({'class': "gt-s"}, "Your name is ", user_id),
                ),
            ),
            Div({'id': "mousetrap"})
        )
    )

def index_view():
    return Div(
        {'id': "mousetrap"},
        *[
            Img({
                'src': f"/static/{asset('img/smol.png')}",
                'class': "cursor_ai",
                'style': f"left: {pos[0]}%; top: {pos[1]}%;"
            }) 
            for user_id, pos in database.items()
        ]
    )

# HANDLERS

async def index(c: Context, w: Writer):
    # user_id = uuid4()
    # bad boy, no user_id until you're grown up
    user_id = fake.name()
    database[user_id] = [20, 20]
    w.cookie("user_id", user_id, httponly=True, secure=True)
    w.html(index_init(user_id))

async def index_cqrs(c: Context, w: Writer):
    async for _ in w.alive(relay.subscribe("refresh")):
        # c("relay msg received")
        # c("the whole db", {'db': database})
        w.patch(index_view())

async def mouse(c: Context, w: Writer):
    # careful, data keeps coming when window inactive
    signals = await c.signals()
    data = signals.get('data')
    if data:
        user_id = c.req.cookies.get('user_id')
        if user_id and user_id in database:
            dx, dy = data
            database[user_id] = [dx, dy]
    w.empty()

# APP

async def refresh(refresh_rate=0.03):
    while True:
        relay.publish("refresh", "")
        await asyncio.sleep(refresh_rate)

async def main():
    database = {} # poor man's reset
    asyncio.create_task(refresh())
    # with RichTracer() as tracer:
    with JsonTracer() as tracer:
        app = Stario(tracer)

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
    run_process(
        Path(__file__).parent,
        target=serve
    )
