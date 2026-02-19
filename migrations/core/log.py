class MigrationLog:
    def __init__(self, log: bool):
        self.log: bool = log
        self.applied_msg = "[O] applied: {}"
        self.skipped_msg = "[X] skipped: {}"
        self.failed_msg  = "[!] failed:  {}"
        self.error_msg   = "[~] error:   {}"
        self.result_msg  = "[R] result:  {}\n    applied:  {}\n    skipped:  {}"

    def _print(self, template: str, *args) -> None:
        if self.log:
            print(template.format(*args))

    def skipped(self, migration_name: str) -> None:
        self._print(self.skipped_msg, migration_name)
    
    def applied(self, migration_name: str) -> None:
        self._print(self.applied_msg, migration_name)
    
    def failed(self, migration_name: str) -> None:
        self._print(self.failed_msg, migration_name)
    
    def message(self, text: str) -> None:
        if self.log:
            print(f"[M] {text}")
    
    def error(self, error: Exception) -> None:
        self._print(self.error_msg, error)
    
    def result(self, count_all: int, count_applied: int, count_skipped: int) -> None:
        _count = count_applied + count_skipped
        _percent = round(_count / count_all * 100, 2)
        self._print(self.result_msg, f"{_count} / {count_all} [{_percent}%]", count_skipped, count_applied)
