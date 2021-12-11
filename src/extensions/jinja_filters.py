from datetime import datetime


class JinjaFilters:
    def init_app(self, app):
        app.jinja_env.filters['time'] = self.format_datetime

    def format_datetime(self, value: datetime, format="%d.%m.%Y %H:%M Uhr"):
        """Format a date time to (Default): d Mon YYYY HH:MM P"""
        if value is None:
            return ""
        return value.strftime(format)


jinja_filters = JinjaFilters()