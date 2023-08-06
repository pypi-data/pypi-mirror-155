import asyncio
from argparse import ArgumentParser
from prompt_toolkit import PromptSession, ANSI
from prompt_toolkit.patch_stdout import patch_stdout


def main():
    global args, parser_join
    parser = ArgumentParser()
    parser.set_defaults(func=parser.print_usage)
    subparsers = parser.add_subparsers()

    parser_serve = subparsers.add_parser('serve')
    parser_serve.set_defaults(func=serve)
    parser_serve.add_argument('-p', '--port', type=int, default=4362, metavar='port')

    parser_join = subparsers.add_parser('join')
    parser_join.set_defaults(func=join)
    parser_join.add_argument('nickname')
    parser_join.add_argument('-d', '--destination', metavar='host[:port]', default='localhost:4362')

    args = parser.parse_args()
    if args.func == parser.print_usage:
        args.func()
    else:
        try:
            try:
                from asyncio import run
            except ImportError:
                asyncio.run_until_complete(args.func())
            else:
                asyncio.run(args.func())
        except KeyboardInterrupt:
            print()


def parse_hostname(default_port, argparser):
    global HOST, PORT
    DEST = args.destination.split(':')
    HOST = DEST[0]
    if len(DEST) == 1:
        PORT = default_port
    elif len(DEST) == 2:
        PORT = DEST[1]
    else:
        argparser.error('invalid hostname ' + args.destination)


def message(msg, nickname):
    return f'\033[1;32m{nickname}\033[0m {msg}'.encode('utf-8')


async def serve():
    HOST = ''
    PORT = args.port
    writers = []
    names = []

    def format_txt(txt, style='public'):
        formatted = {
            'public': f'\033[1;36m{txt}\033[0m',
            'private': f'\033[1;35m{txt}\033[0m',
            'error': f'\033[1;31m{txt}\033[0m'
        }
        return formatted[style].encode('utf-8')

    async def send(x, writer):
        writer.write(x)
        await writer.drain()

    async def broadcast(x, excepted=None):
        await asyncio.gather(*[send(x, writer) for writer in writers if writer != excepted])

    async def handler(reader, writer):
        nickname = (await reader.read(1024)).decode('utf-8')
        if not (nickname.isalnum() and not nickname.isdigit()) or nickname in names:
            await send(format_txt('Your nickname is not available.', 'error'), writer)
            writer.close()
            return
        await send(format_txt('You are now in the chat room.', 'private'), writer)
        task_broadcast_join = asyncio.create_task(broadcast(format_txt(f'{nickname} has joined the chat.'), writer))
        writers.append(writer)
        names.append(nickname)
        while True:
            msg = (await reader.read(1024)).decode('utf-8')
            if not msg:
                writers.remove(writer)
                names.remove(nickname)
                writer.close()
                await task_broadcast_join
                await broadcast(format_txt(f'{nickname} has left the chat.'), writer)
                break
            for char in '\a\b\f\n\r\t\v\0':
                msg = msg.replace(char, '')
            if msg.isspace():
                continue
            asyncio.create_task(broadcast(message(msg, nickname)))

    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        await server.serve_forever()


async def join():
    parse_hostname(4362, parser_join)
    NICKNAME = args.nickname

    async def receiver():
        try:
            while True:
                x = (await reader.read(1024)).decode('utf-8')
                if not x:
                    print('\033[1;31mConnection lost.\033[0m')
                    raise RuntimeError
                print(x)
        except asyncio.CancelledError:
            ...

    async def sender():
        session = PromptSession(ANSI(message('', NICKNAME).decode('utf-8')))
        try:
            while True:
                msg = await session.prompt_async()
                session.output.cursor_up(1)
                print('\033[K', end='')
                writer.write(msg.encode('utf-8'))
                await writer.drain()
        except (EOFError, KeyboardInterrupt):
            raise RuntimeError
        except asyncio.CancelledError:
            ...

    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
    except OSError:
        print('\033[1;31mConnect call failed.\033[0m')
    else:
        writer.write(NICKNAME.encode('utf-8'))
        await writer.drain()
        with patch_stdout(True):
            try:
                future = asyncio.gather(receiver(), sender())
                await future
            except RuntimeError:
                future.cancel()


if __name__ == '__main__':
    main()
