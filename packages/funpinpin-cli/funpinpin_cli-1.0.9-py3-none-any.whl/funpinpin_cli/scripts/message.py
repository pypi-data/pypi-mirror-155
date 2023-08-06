"""command message."""
import shutil

import click

from funpinpin_cli.config import DOMAIN_SUFFIX

columns, lines = shutil.get_terminal_size()

ERROR_LEFT_TOP = "┏━━━━ Error "
ERROR_LEFT_FIR = "┃ x "
ERROR_LEFT_MID = "┃ "
ERROR_LEFT_BOT = "┗"

ERROR_TOP = (
    click.style(ERROR_LEFT_TOP, fg="red") +
    click.style("━" * (columns - len(ERROR_LEFT_TOP)), fg="red") +
    "\n"
)
ERROR_FIR = click.style(ERROR_LEFT_FIR, fg="red")
ERROR_MID = click.style(ERROR_LEFT_MID, fg="red")
ERROR_BOT = (
    click.style(ERROR_LEFT_BOT, fg="red") +
    click.style("━" * (columns - len(ERROR_LEFT_BOT)), fg="red")
)

MSG_NO_STORE = (
    ERROR_TOP +
    ERROR_FIR +
    click.style("No store found. Please run", fg="red") +
    " " +
    click.style("funpinpin login --store STORE", fg="bright_cyan") +
    click.style(" to login to a specific store", fg="red") +
    "\n" +
    ERROR_BOT
)

MSG_NO_PARTNER = (
    "It doesn't appear that you're logged in. " +
    "You must log into a partner organization or a store staff account.\n" +
    "\n" +
    "If trying to log into a store staff account, please use " +
    click.style("funpinpin login --store STORE", fg="bright_cyan") +
    " to log in."
)


def get_login_msg(shop, partner_name):
    """Get login shop successfully message."""
    if not shop:
        msg = (
            "Logged into partner organization " +
            click.style(f"{partner_name}", fg="green")
        )
    else:
        msg = (
            "Logged into store " +
            click.style(f"{shop} ", fg="green") +
            "in partner organization " +
            click.style(f"{partner_name}", fg="green")
        )
    return msg


def wrap_msg(msg):
    """Wrap display message."""
    msg_formatted = ERROR_TOP
    # ToDo:
    # if there is special style, such as underline or color,
    # tranverse msg, assign new style.
    # Tmporarily, assign red.
    if (len(msg) + len(ERROR_LEFT_FIR) - columns) <= 0:
        msg_formatted += (
            ERROR_FIR +
            click.style(msg, fg="red") + "\n" +
            ERROR_BOT
        )
    else:
        msg_formatted += (
            ERROR_FIR + click.style(msg[:columns - 4], fg="red") + "\n"
        )
        msg_left = len(msg) - columns + len(ERROR_LEFT_FIR)
        msg_lines = msg_left // (columns - 2)
        j = columns - 4
        for i in range(msg_lines):
            msg_mid = ERROR_MID + click.style(
                msg[j: j + columns - 2] + "\n", fg="red"
            )
            msg_formatted += msg_mid
            j += (columns - 2)
        if j <= len(msg):
            msg_last = ERROR_MID + click.style(
                msg[j:] + "\n", fg="red"
            )
            msg_formatted += msg_last
        msg_formatted += ERROR_BOT
    return msg_formatted


def get_invalid_shop_msg(shop):
    """Get invalid shop message."""
    msg = (
        f"Invalid store provided ({shop}). " +
        "Please provide the store in the following format: " +
        f"my-store.v3.myfunpinpin.{DOMAIN_SUFFIX}"
    )
    return wrap_msg(msg)


def get_populate_begin_msg(shop):
    """Get message before populate."""
    msg = \
        "Proceeding using " + click.style(f"{shop}", fg="green")
    return msg


def get_populate_msg(shop, obj_type, obj_name, obj_id):
    """Get obj message when created successfully."""
    msg = \
        f"{obj_name} added to " + \
        click.style(f"{shop}", fg="green") + \
        " at " + \
        click.style(
            f"https://{shop}/admin/{obj_type}/{obj_id}",
            underline=True
        )
    return msg


def get_populate_end_msg(shop, obj_type, count):
    """Get message after populate."""
    msg = (
        f"Successfully added {count} {obj_type.capitalize()} to " +
        click.style(f"{shop}\n", fg="green") +
        "View all Products at " +
        click.style(f"https://{shop}/admin/{obj_type}", underline=True)
    )
    return msg


def get_switch_same_strore_msg(shop):
    """Get message when switch to the same store."""
    msg = \
        "Using development store " + \
        click.style(f"{shop}\n", fg="green") + \
        "Switched development store to " + \
        click.style(f"{shop}", fg="green")
    return msg


def get_ngrok_auth_error_msg():
    """Get ngrok auth error message."""
    msg = (
        "A free ngrok account is required: " +
        "https://ngrok.com/signup. After you signup, " +
        "install your personal authorization token using " +
        "funpinpin app tunnel auth <token>."
    )
    return wrap_msg(msg)


def get_ngrok_run_msg(account, url):
    """Get ngrok run message."""
    msg = (
        "ngrok tunnel running at " +
        click.style(f"{url}", underline=True) +
        f", with account {account}"
    )
    return msg


NGROK_CANNOT_STOPPED_MSG = (
    click.style(
        "ngrok tunnel could not be stopped. Try running ", fg="red"
    ) +
    click.style("killall -9 ngrok", fg="bright_cyan")
)


def get_ngrok_108_msg():
    """Get ngrok 108 error message."""
    msg = (
        "Another ngrok tunnel is currently running with your auth token," +
        " possibly on another machine. " +
        "Terminate that tunnel before opening a new one."
    )
    return wrap_msg(msg)


def get_ngrok_107_msg():
    """Get ngrok 107 error message."""
    msg = (
        "The ngrok token currently configured is invalid. " +
        "After generating a new token, " +
        "update your local ngrok configuration " +
        "using shopify app tunnel auth <token>"
    )
    return wrap_msg(msg)
