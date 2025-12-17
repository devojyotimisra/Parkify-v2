import random
from application.helpers.models import User, ReserveParkingSpot, ParkingLot
from celery.schedules import crontab
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import render_template
import csv
import smtplib
import io


class BackgroundJobs:
    def __init__(self, celery, app):
        self.celery = celery
        self.app = app
        self._register_tasks()

    def _register_tasks(self):
        @self.celery.task
        def export_csv_task(user_id):
            with self.app.app_context():
                return self.export_csv(user_id)

        @self.celery.task
        def daily_reminder_task():
            with self.app.app_context():
                return self.daily_reminder()

        @self.celery.task
        def monthly_report_task():
            with self.app.app_context():
                return self.monthly_report()

        @self.celery.task
        def booking_confirmation_email_task(reservation_id):
            with self.app.app_context():
                return self.booking_confirmation_email(reservation_id)

        @self.celery.task
        def slot_release_email_task(reservation_id):
            with self.app.app_context():
                return self.slot_release_email(reservation_id)

        self.export_csv_task = export_csv_task
        self.daily_reminder_task = daily_reminder_task
        self.monthly_report_task = monthly_report_task
        self.booking_confirmation_email_task = booking_confirmation_email_task
        self.slot_release_email_task = slot_release_email_task

    def send_email(self, recipient, subject, body, attachment_data=None, attachment_filename=None):
        msg = MIMEMultipart()
        msg["From"] = self.app.config["SENDER_EMAIL"]
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        if attachment_data and attachment_filename:
            attachment = MIMEBase('application', 'octet-stream')

            if isinstance(attachment_data, str):
                attachment.set_payload(attachment_data.encode('utf-8'))

            else:
                attachment.set_payload(attachment_data)

            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={attachment_filename}')
            msg.attach(attachment)

        try:
            if int(self.app.config.get("MAIL_PORT", 0)) == 465:
                server_class = smtplib.SMTP_SSL
            else:
                server_class = smtplib.SMTP

            with server_class(host=self.app.config["MAIL_SERVER"], port=self.app.config["MAIL_PORT"]) as server:
                if int(self.app.config.get("MAIL_PORT", 0)) == 587:
                    server.starttls()
                server.login(self.app.config["SENDER_EMAIL"], self.app.config["SENDER_PASSWORD"])
                server.send_message(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

    def export_csv(self, user_id):
        user = User.query.get(user_id)

        if not user:
            return None

        reservations = ReserveParkingSpot.query.filter_by(user_id=user_id).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Reservation ID', 'Lot ID', 'Lot Name', 'Lot Address', 'Spot ID', 'Vehicle Number', 'Parking Timestamp', 'Leaving Timestamp', 'Duration (Hours)', 'Cost Per Hour', 'Total Cost', 'Status'])

        for res in reservations:
            lot = ParkingLot.query.get(res.lot_id) if res.lot_id else None
            lot_name = lot.prime_location_name if lot else "Out of Service"
            lot_address = lot.address if lot else "Out of Service"
            parking_time = res.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S") if res.parking_timestamp else ""
            leaving_time = res.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if res.leaving_timestamp else ""
            status = "Completed" if res.leaving_timestamp else "Active"
            writer.writerow([
                res.id,
                res.lot_id or "Out of Service",
                lot_name,
                lot_address,
                res.spot_id or "Out of Service",
                res.vehicle_number,
                parking_time,
                leaving_time,
                f"{res.duration_hours:.2f}" if res.duration_hours else "",
                f"{res.parking_cost_per_unit_time:.2f}",
                f"{res.total_cost:.2f}" if res.total_cost else "",
                status
            ])

        csv_content = output.getvalue()
        output.close()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"parkify_{timestamp}.csv"
        subject = "Your Parkify Parking History Export"
        body = render_template('email_csv_export.html', user_name=user.name, record_count=len(reservations), frontend_url=self.app.config["FRONTEND_URL"])

        self.send_email(
            recipient=user.email,
            subject=subject,
            body=body,
            attachment_data=csv_content,
            attachment_filename=filename
        )

        return "Sent exported CSV"

    def daily_reminder(self):
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        today_start = datetime.now(ist_tz).replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now(ist_tz).replace(hour=23, minute=59, second=59, microsecond=999999)
        all_users = User.query.filter_by(active=True).all()
        all_lots = ParkingLot.query.all()
        spot_of_the_day = random.choice(all_lots) if all_lots else None
        tips = [
            "Always check your mirrors before opening your car door.",
            "Park in a well-lit area for better safety at night.",
            "Reverse parking makes it safer and easier to leave.",
            "Don't forget to lock your car and close all windows.",
            "Keep valuables out of sight to prevent break-ins.",
            "Check your tire pressure regularly for better fuel efficiency.",
            "Use your parking brake, especially on inclines."
        ]
        tip_of_the_day = random.choice(tips)
        emails_sent = 0

        for user in all_users:
            if user.has_role('admin'):
                continue

            today_reservations = ReserveParkingSpot.query.filter(
                ReserveParkingSpot.user_id == user.id,
                ReserveParkingSpot.parking_timestamp >= today_start,
                ReserveParkingSpot.parking_timestamp <= today_end
            ).first()

            if not today_reservations:
                continue

            subject = "Parkify Daily Pulse - Lot of the Day & Tips"
            body = render_template(
                'email_daily_reminder.html',
                user_name=user.name,
                spot=spot_of_the_day,
                tip=tip_of_the_day,
                frontend_url=self.app.config["FRONTEND_URL"]
            )
            self.send_email(recipient=user.email, subject=subject, body=body)
            emails_sent += 1

        return f"Sent {emails_sent} daily reminders"

    def monthly_report(self):
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        today = datetime.now(ist_tz)
        first_day_this_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_year = today.strftime("%B %Y")
        all_users = User.query.filter_by(active=True).all()
        emails_sent = 0

        for user in all_users:
            if user.has_role('admin'):
                continue

            monthly_reservations = ReserveParkingSpot.query.filter(
                ReserveParkingSpot.user_id == user.id,
                ReserveParkingSpot.parking_timestamp >= first_day_this_month,
                ReserveParkingSpot.parking_timestamp <= today,
                ReserveParkingSpot.leaving_timestamp.isnot(None)
            ).all()

            total_bookings = len(monthly_reservations)
            total_spent = sum(res.total_cost or 0 for res in monthly_reservations)
            total_hours = sum(res.duration_hours or 0 for res in monthly_reservations)
            lot_usage = {}

            for res in monthly_reservations:
                lot_id = res.lot_id
                if lot_id:
                    lot_usage[lot_id] = lot_usage.get(lot_id, 0) + 1

            most_used_lot_id = max(lot_usage, key=lot_usage.get) if lot_usage else None
            most_used_lot = ParkingLot.query.get(most_used_lot_id) if most_used_lot_id else None
            most_used_lot_name = most_used_lot.prime_location_name if most_used_lot else "N/A"
            most_used_count = lot_usage.get(most_used_lot_id, 0) if most_used_lot_id else 0
            bookings = []

            for res in monthly_reservations[:10]:
                lot = ParkingLot.query.get(res.lot_id) if res.lot_id else None
                bookings.append({
                    'date': res.parking_timestamp.strftime("%d %b %Y"),
                    'location': lot.prime_location_name if lot else "Out of Service",
                    'duration': f"{res.duration_hours:.1f}h" if res.duration_hours else "N/A",
                    'cost': f"{res.total_cost:.2f}" if res.total_cost else "N/A"
                })

            parker_badge = "Casual Cruiser"
            
            if total_bookings > 10:
                parker_badge = "Parking Pro"

            elif total_bookings > 2:
                parker_badge = "Regular Rider"

            subject = f"Your Parkify Monthly Rewind - {month_year}"
            body = render_template(
                'email_monthly_report.html',
                user_name=user.name,
                month_year=month_year,
                total_bookings=total_bookings,
                total_spent=total_spent,
                total_hours=total_hours,
                most_used_lot=most_used_lot_name,
                most_used_count=most_used_count,
                bookings=bookings,
                parker_badge=parker_badge,
                frontend_url=self.app.config["FRONTEND_URL"]
            )

            self.send_email(recipient=user.email, subject=subject, body=body)
            emails_sent += 1

        return f"Sent {emails_sent} monthly reports"

    def booking_confirmation_email(self, reservation_id):
        reservation = ReserveParkingSpot.query.get(reservation_id)
        if not reservation:
            return "Reservation not found"

        user = User.query.get(reservation.user_id)
        lot = ParkingLot.query.get(reservation.lot_id)

        subject = "Booking Confirmed - Parkify"
        body = render_template(
            'email_booking_confirmation.html',
            user_name=user.name,
            lot_name=lot.prime_location_name,
            lot_address=lot.address,
            spot_id=reservation.spot_id,
            vehicle_number=reservation.vehicle_number,
            start_time=reservation.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            reservation_id=reservation.id,
            frontend_url=self.app.config["FRONTEND_URL"]
        )

        self.send_email(recipient=user.email, subject=subject, body=body)
        return f"Sent booking confirmation to {user.email}"

    def slot_release_email(self, reservation_id):
        reservation = ReserveParkingSpot.query.get(reservation_id)
        if not reservation:
            return "Reservation not found"

        user = User.query.get(reservation.user_id)
        lot = ParkingLot.query.get(reservation.lot_id) if reservation.lot_id else None

        subject = "Parking Session Ended - Parkify"
        body = render_template(
            'email_slot_release.html',
            user_name=user.name,
            lot_name=lot.prime_location_name,
            lot_address=lot.address,
            duration=f"{reservation.duration_hours:.2f}",
            total_cost=f"{reservation.total_cost:.2f}",
            end_time=reservation.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            start_time=reservation.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            vehicle_number=reservation.vehicle_number,
            reservation_id=reservation.id,
            spot_id=reservation.spot_id,
            frontend_url=self.app.config["FRONTEND_URL"]
        )

        self.send_email(recipient=user.email, subject=subject, body=body)
        return f"Sent slot release email to {user.email}"

    def setup_periodic_tasks(self):
        self.celery.conf.beat_schedule = {
            'daily-reminder': {'task': self.daily_reminder_task.name, 'schedule': crontab(hour=17, minute=59)},
            'monthly-report': {'task': self.monthly_report_task.name, 'schedule': crontab(hour=17, minute=59, day_of_month=30)}
        }
