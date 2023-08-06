import itertools, time, os, shutil
import threading


class Loader:
    def __init__(self, loading_msg='Loading...', end_msg='Done!', error_msg='Error Occoured', latency=0.05):

        self.loading_msg = loading_msg
        self.end_msg = end_msg
        self.error_msg = error_msg
        self.latency = latency

        self.steps = ['[-]', '[\\]', '[|]', '[/]']
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self.done = False
        self.error = ''
        self.force_quit = False
        self.previous_output = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in itertools.cycle(self.steps):
            if self.done:
                break
            print(f'\r{c} {self.loading_msg}', flush=True, end='')
            time.sleep(self.latency)

    def __enter__(self):
        self.start()
        return self

    def stop(self):
        self.done = True
        # cols = shutil.get_terminal_size((80, 20)).columns
        print("\r" + " " * (len(self.loading_msg)+4), end="", flush=True) # Needs Checking
        if not self.previous_output:
            if self.force_quit:
                print(f"\r[-] {self.error_msg}", flush=True)
                self.previous_output = True
            else:
                print(f"\r[✓] {self.end_msg}", flush=True)
                self.previous_output = True

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

    def cancel(self, error='Unknown Error'):
        self.error = error
        self.force_quit = True
        self.stop()
