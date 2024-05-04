# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime

# Pyjnius for Android notifications
from jnius import autoclass, cast

class NotificationApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Waiting for 15:00...")
        self.layout.add_widget(self.label)
        Clock.schedule_interval(self.check_time, 1)
        return self.layout

    def check_time(self, dt):
        now = datetime.now()
        if now.hour == 15 and now.minute == 0:
            self.show_notification("Notification", "It's 15:00!")
        else:
            self.label.text = f"{now.hour}:{now.minute:02d}:{now.second:02d}"

    def show_notification(self, title, message):
        Context = autoclass('android.content.Context')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationManager = autoclass('android.app.NotificationManager')

        current_activity = cast(Context, PythonActivity.mActivity)
        notification_service = cast(NotificationManager,
                                    current_activity.getSystemService(Context.NOTIFICATION_SERVICE))

        notification = NotificationBuilder(current_activity)
        notification.setContentTitle(title)
        notification.setContentText(message)
        notification.setSmallIcon(current_activity.getApplicationInfo().icon)
        notification.setAutoCancel(True)
        notification_service.notify(0, notification.build())


if __name__ == '__main__':
    NotificationApp().run()
