import csv
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.config import ADMIN_USER_ID
from app.database.db import get_connection


# =========================
# LEADS COMMAND
# =========================
async def leads_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Admin check
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, service, contact, status, created_at
        FROM project_requests
        ORDER BY id DESC
    """)
    leads = cursor.fetchall()
    connection.close()

    if not leads:
        await update.message.reply_text("📭 No project requests found.")
        return

    for lead in leads:
        keyboard = [
            [InlineKeyboardButton("👁 View Details", callback_data=f"view_lead_{lead['id']}")],
            [InlineKeyboardButton("📊 Change Status", callback_data=f"status_lead_{lead['id']}")],
            [InlineKeyboardButton("🗑 Delete Lead", callback_data=f"delete_lead_{lead['id']}")]
        ]

        message = f"""
📩 Project Request #{lead['id']}

👤 {lead['name']}
💼 {lead['service']}
📞 {lead['contact']}

📊 Status: {lead['status']}
🕒 {lead['created_at']}
"""

        await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))


# =========================
# LEAD COMMAND
# =========================
async def lead_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Please provide a lead ID.\n\nExample:\n/lead 3")
        return

    try:
        lead_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Lead ID must be a number.\n\nExample:\n/lead 3")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, service, requirement, contact,
               telegram_user_id, telegram_username, created_at
        FROM project_requests
        WHERE id = ?
    """, (lead_id,))
    lead = cursor.fetchone()
    connection.close()

    if not lead:
        await update.message.reply_text(f"❌ Lead #{lead_id} was not found.")
        return

    username = f"@{lead['telegram_username']}" if lead["telegram_username"] else "Not available"

    message = f"""
📩 Project Request #{lead['id']}

👤 Name: {lead['name']}
💼 Service: {lead['service']}
📝 Requirement: {lead['requirement']}
📞 Contact: {lead['contact']}

👨‍💻 Telegram: {username}
🆔 Telegram User ID: {lead['telegram_user_id']}
🕒 Submitted: {lead['created_at']}
"""

    await update.message.reply_text(message)


# =========================
# ADMIN CALLBACK HANDLER
# =========================
async def admin_lead_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    if user.id != ADMIN_USER_ID:
        await query.answer("❌ Unauthorized", show_alert=True)
        return

    data = query.data

    # ---- CHANGE STATUS ----
    if data.startswith("status_lead_"):
        lead_id = int(data.replace("status_lead_", ""))
        keyboard = [
            [InlineKeyboardButton("🆕 New", callback_data=f"set_status_{lead_id}_New")],
            [InlineKeyboardButton("🔄 Contacted", callback_data=f"set_status_{lead_id}_Contacted")],
            [InlineKeyboardButton("💬 In Discussion", callback_data=f"set_status_{lead_id}_Discussion")],
            [InlineKeyboardButton("✅ Converted", callback_data=f"set_status_{lead_id}_Converted")],
            [InlineKeyboardButton("❌ Closed", callback_data=f"set_status_{lead_id}_Closed")],
            [InlineKeyboardButton("⬅️ Cancel", callback_data=f"cancel_status_{lead_id}")]
        ]
        await query.edit_message_text(f"📊 Change status for Lead #{lead_id}", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # ---- SET STATUS ----
    if data.startswith("set_status_"):
        _, _, lead_id, status = data.split("_", 3)
        lead_id = int(lead_id)

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE project_requests SET status = ? WHERE id = ?", (status, lead_id))
        connection.commit()
        updated = cursor.rowcount
        connection.close()

        if updated:
            await query.edit_message_text(f"✅ Lead #{lead_id} status updated to:\n\n📊 {status}")
        else:
            await query.edit_message_text(f"❌ Lead #{lead_id} was not found.")
        return

    # ---- CANCEL STATUS ----
    if data.startswith("cancel_status_"):
        lead_id = int(data.replace("cancel_status_", ""))
        await query.edit_message_text(f"❌ Status change cancelled for Lead #{lead_id}.")
        return

    # ---- VIEW LEAD ----
    if data.startswith("view_lead_"):
        lead_id = int(data.replace("view_lead_", ""))
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, name, service, requirement, contact,
                   telegram_user_id, telegram_username, created_at
            FROM project_requests
            WHERE id = ?
        """, (lead_id,))
        lead = cursor.fetchone()
        connection.close()

        if not lead:
            await query.edit_message_text("❌ This lead no longer exists.")
            return

        username = f"@{lead['telegram_username']}" if lead["telegram_username"] else "Not available"
        message = f"""
📩 Project Request #{lead['id']}

👤 Name: {lead['name']}
💼 Service: {lead['service']}
📝 Requirement: {lead['requirement']}
📞 Contact: {lead['contact']}

👨‍💻 Telegram: {username}
🆔 Telegram User ID: {lead['telegram_user_id']}
🕒 Submitted: {lead['created_at']}
"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Leads", callback_data="admin_leads")]]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # ---- DELETE LEAD ----
    if data.startswith("delete_lead_"):
        lead_id = int(data.replace("delete_lead_", ""))
        keyboard = [
            [InlineKeyboardButton("✅ Yes, Delete", callback_data=f"confirm_delete_{lead_id}"),
             InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_delete_{lead_id}")]
        ]
        await query.edit_message_text(f"⚠️ Are you sure you want to delete Lead #{lead_id}?", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # ---- CANCEL DELETE ----
    if data.startswith("cancel_delete_"):
        lead_id = int(data.replace("cancel_delete_", ""))
        await query.edit_message_text(f"❌ Deletion cancelled for Lead #{lead_id}.")
        return

    # ---- CONFIRM DELETE ----
    if data.startswith("confirm_delete_"):
        lead_id = int(data.replace("confirm_delete_", ""))
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM project_requests WHERE id = ?", (lead_id,))
        connection.commit()
        deleted = cursor.rowcount
        connection.close()

        if deleted:
            await query.edit_message_text(f"🗑 Lead #{lead_id} deleted successfully.")
        else:
            await query.edit_message_text(f"❌ Lead #{lead_id} was not found.")
        return

    # ---- BACK TO LEADS ----
    if data == "admin_leads":
        await query.edit_message_text("📋 Use /leads to refresh the lead list.")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # Admin check
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    connection = get_connection()
    cursor = connection.cursor()

    # Total leads
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM project_requests
    """)
    total = cursor.fetchone()["total"]

    # Leads by status
    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM project_requests
        GROUP BY status
    """)

    status_rows = cursor.fetchall()

    connection.close()

    # Default values
    status_counts = {
        "New": 0,
        "Contacted": 0,
        "Discussion": 0,
        "Converted": 0,
        "Closed": 0,
    }

    for row in status_rows:
        if row["status"] in status_counts:
            status_counts[row["status"]] = row["count"]

    message = f"""
📊 Lead Statistics

📩 Total Leads: {total}

🆕 New: {status_counts['New']}
🔄 Contacted: {status_counts['Contacted']}
💬 In Discussion: {status_counts['Discussion']}
✅ Converted: {status_counts['Converted']}
❌ Closed: {status_counts['Closed']}
"""

    await update.message.reply_text(message)



async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # Admin check
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            service,
            requirement,
            contact,
            telegram_user_id,
            telegram_username,
            status,
            created_at
        FROM project_requests
        ORDER BY id DESC
    """)

    leads = cursor.fetchall()
    connection.close()

    if not leads:
        await update.message.reply_text(
            "📭 No leads available to export."
        )
        return

    file_path = Path("project_leads.csv")

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # CSV header
        writer.writerow([
            "ID",
            "Name",
            "Service",
            "Requirement",
            "Contact",
            "Telegram User ID",
            "Telegram Username",
            "Status",
            "Created At",
        ])

        # Lead data
        for lead in leads:
            writer.writerow([
                lead["id"],
                lead["name"],
                lead["service"],
                lead["requirement"],
                lead["contact"],
                lead["telegram_user_id"],
                lead["telegram_username"],
                lead["status"],
                lead["created_at"],
            ])

    with open(file_path, "rb") as file:
        await update.message.reply_document(
            document=file,
            filename="project_leads.csv",
            caption="📊 Your project leads export."
        )

        from pathlib import Path

    file_path = Path(__file__).resolve().parent.parent.parent / "project_leads.csv"

    with open(file_path, "rb") as file:
        await update.message.reply_document(
            document=file,
            filename="project_leads.csv",
            caption="📊 Your project leads export."
        )
