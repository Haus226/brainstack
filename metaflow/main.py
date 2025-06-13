from metaflow import FlowSpec, step
class HelloWorldFlow(FlowSpec):
    @step
    def start(self):
        print("Hello, World!")
        self.next(self.end)

    @step
    def end(self):
        print("Flow has ended.")
HelloWorldFlow()
