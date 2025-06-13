import socket
import threading
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

HOST = '192.168.1.115'
PORT = 5000

console = Console()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    console.print("[bold red]Connection refused. Is the server running?[/bold red]")
    sys.exit(1)

name = input("Enter your name: ")
client.send(name.encode())

def receive_messages():
    while True:
        try:
            msg = client.recv(4096).decode()
            if not msg:
                break
            
            # Create the message panel first
            if ":" in msg:
                sender, content = msg.split(":", 1)
                print(sender)
                sender = "Me" if sender == f"<{name}>" else sender
                now = datetime.now().strftime('%H:%M:%S')
                panel = Panel(Text(content.strip(), justify="left"), title=f"[bold green][{now}]{sender}[/bold green]", border_style="blue")
            else:
                panel = Panel(Text(msg, justify="center"), style="bold magenta")
            console.print(panel)

        except (ConnectionResetError, BrokenPipeError):
            console.print("\n[bold red]Connection to the server was lost.[/bold red]")
            break
        except Exception as e:
            console.print(f"\n[bold red]An error occurred: {e}[/bold red]")
            break

def send_messages():
    while True:
        try:
            message = console.input()
            sys.stdout.write('\033[F')  # Move cursor up 1 line
            sys.stdout.write('\r' + ' ' * 100 + '\r')  # Clear the line
            if message.lower() == 'exit':
                client.close()
                break
            if message.strip():
                if message.startswith("/msg"):
                    try:
                        _, recipient, private_msg = message.split(" ", 2)
                        client.send(f"/msg:{recipient}:{private_msg}".encode())
                        console.print(Panel(f"to {recipient}: {private_msg}", title="[bold yellow]Private Message Sent[/bold yellow]", border_style="yellow"))
                    except ValueError:
                        console.print("[bold red]Invalid private message format. Use: /msg <user> <message>[/bold red]")
                else:
                    client.send(message.encode())
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold orange3]You have left the chat.[/bold orange3]")
            client.close()
            break


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    send_thread = threading.Thread(target=send_messages)

    receive_thread.start()
    send_thread.start()
    receive_thread.join()  # Wait for the receive_thread to finish
    send_thread.join()  # Wait for the send_thread to finish

    console.print("[bold blue]Disconnected from the server.[/bold blue]")