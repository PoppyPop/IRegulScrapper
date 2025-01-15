import sys
import asyncio
import aiofiles


async def get_datas():
    reader, writer = await asyncio.open_connection("i-regul.fr", 443, limit=128 * 1024)

    messagecode = 501
    message = f"cdraminfo106949TWHQWC{{{messagecode}#}}"
    writer.write(message.encode())
    await writer.drain()

    while True:
        try:
            msg = await reader.readuntil(b"}")
        except asyncio.LimitOverrunError as e:
            print(e)
            sys.exit(1)
        except asyncio.IncompleteReadError as e:
            # Something else happened, handle error, exit, etc.
            print(e)
            sys.exit(1)
        else:
            if len(msg) == 0:
                print("orderly shutdown on server end")
                sys.exit(0)
            else:
                decoded = msg.decode("utf-8")
                if decoded.startswith("OLD"):
                    print(f"Get old mesage of {len(decoded)} bytes")
                    async with aiofiles.open(
                        f"{messagecode}-OLD.txt", mode="w", encoding="utf-8"
                    ) as f:
                        await f.write(decoded)
                else:
                    print(f"Get new mesage of {len(decoded)} bytes")
                    async with aiofiles.open(
                        f"{messagecode}-NEW.txt", mode="w", encoding="utf-8"
                    ) as f:
                        await f.write(decoded)
                    break

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


asyncio.run(get_datas())

# create an INET, STREAMing socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(5)
# # now connect to the web server on port 80 - the normal http port
# s.connect(("i-regul.fr", 443))

# # 500
# 501 => request DATA refresh
# 502 => DATA + Nom propre
# {203#} => Degivrage


# {550#}" : "{540#}" : "{530#}" : "{520#}" : "{510#}

# s.send("cdraminfo106949TWHQWC{502#}".encode())

# while True:
#     try:
#         msg = s.recv(8192)
#     except socket.timeout as e:
#         err = e.args[0]
#         # this next if/else is a bit redundant, but illustrates how the
#         # timeout exception is setup
#         if err == "timed out":
#             sleep(1)
#             print("recv timed out, retry later")
#             continue
#         else:
#             print(e)
#             sys.exit(1)
#     except socket.error as e:
#         # Something else happened, handle error, exit, etc.
#         print(e)
#         sys.exit(1)
#     else:
#         if len(msg) == 0:
#             print("orderly shutdown on server end")
#             sys.exit(0)
#         else:
#             print(msg.decode("utf-8"))
