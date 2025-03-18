import threading
import datetime
import os
from abc import ABC, abstractmethod

class LogEntry:
    def __init__(self, timestamp, type_, source, message):
        self.timestamp = timestamp
        self.type = type_
        self.source = source
        self.message = message

class LogBuilder(ABC):
    @abstractmethod
    def build(self, log_entry: LogEntry) -> str:
        pass

class TextLogBuilder(LogBuilder):
    def build(self, log_entry):
        return f"{log_entry.timestamp} [{log_entry.type}] ({log_entry.source}): {log_entry.message}\n"

class XmlLogBuilder(LogBuilder):
    def build(self, log_entry):
        return f'''<entry>
    <timestamp>{log_entry.timestamp}</timestamp>
    <type>{log_entry.type}</type>
    <source>{log_entry.source}</source>
    <message>{log_entry.message}</message>
</entry>'''

class Logger:
    def __init__(self, log_file, log_builder):
        self.log_file = log_file
        self.log_builder = log_builder
        self.lock = threading.Lock()
        if isinstance(log_builder, XmlLogBuilder) and not os.path.exists(log_file):
            with self.lock:
                with open(log_file, 'w') as f:
                    f.write('<log>\n</log>')

    def log(self, type_, source, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = LogEntry(timestamp, type_, source, message)
        log_content = self.log_builder.build(log_entry)

        with self.lock:
            if isinstance(self.log_builder, XmlLogBuilder):
                if os.path.exists(self.log_file):
                    with open(self.log_file, 'r+') as f:
                        content = f.read()
                        content = content.replace('</log>', '')
                        content += log_content + '\n</log>'
                        f.seek(0)
                        f.write(content)
                        f.truncate()
                else:
                    with open(self.log_file, 'w') as f:
                        f.write('<log>\n')
                        f.write(log_content + '\n</log>')
            else:
                with open(self.log_file, 'a') as f:
                    f.write(log_content)

if __name__ == "__main__":
    text_logger = Logger('log.txt', TextLogBuilder())
    xml_logger = Logger('log.xml', XmlLogBuilder())

    def worker(name):
        text_logger.log('INFO', name, f'Worker {name} started.')
        xml_logger.log('WARNING', name, f'Worker {name} is doing something.')
        xml_logger.log('ERROR', name, f'Worker {name} encountered an error.')

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(f'Worker-{i}',))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
