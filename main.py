import json
import asyncio
from pathlib import Path

from watchfiles import run_process

from stario import Context, RichTracer, Stario, Writer, JsonTracer
from stario.http.router import Router

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
    Script,
    Source,
    Span,
    Style,
    Title,
    Ul,
    Video
)


def index_view():
    return Html(
        {"lang": "en"},
        Head(
            # Meta({'charset': "UTF-8"}),
            # Meta(
            #     {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            # ),
            # Title("leg.ovh"),
            # Link({
            #     'rel': "icon",
            #     'href': f"/static/{asset('img/avatar.avif')}"
            # }),
            # Link({
            #     'rel': "stylesheet",
            #     'href': f"/static/{asset('css/index.css')}"
            # }),
            # Script({
            #     'type': "module",
            #     'src': f"/static/{asset('js/datastar.js')}"
            # }),
            # Script({
            #     'type': "module",
            #     'src': f"/static/{asset('js/index.js')}"
            # }),
        ),
        Body(
            Main()
        )
    )

# HANDLERS

async def index(c: Context, w: Writer):
    w.html(index_view())

# APP

async def main():
    # with RichTracer() as tracer:
    with JsonTracer() as tracer:
        app = Stario(tracer)

        app.get("/", index)

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
