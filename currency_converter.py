import tkinter as tk
import http.client


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.currencies = ["HRK", "EUR", "USD", "GBP", "AUD", "CNY"]
        self.input_currency = tk.StringVar()
        self.output_currency = tk.StringVar()
        self.input_currency.set("EUR")
        self.output_currency.set("USD")

        validate_command = self.register(self.validate_digits)
        label_var1 = tk.StringVar()
        label_var1.set("Currency from: ")
        label_var2 = tk.StringVar()
        label_var2.set("Currency to: ")
        self.from_label = tk.Label(self, textvariable=label_var1)
        self.to_label = tk.Label(self, textvariable=label_var2)

        self.entry = tk.Entry(self, validate="key", validatecommand=(validate_command, '%d', '%P'))
        self.currency_from = tk.OptionMenu(self, self.input_currency, *self.currencies)
        self.currency_to = tk.OptionMenu(self, self.output_currency, *self.currencies)
        self.convert_button = tk.Button(self, text="Convert", command=self.convert, height=2)
        self.output_value = tk.StringVar()
        self.output_value.set("Converted currency amount will appear here")
        self.output_label = tk.Label(self, textvariable=self.output_value)
        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.pack()
        self.create_widgets()


    def validate_digits(self, action, value_if_allowed):
        if action == '1':
            try:
                float(value_if_allowed)
            except ValueError:
                return False
        return True


    def create_widgets(self):
        self.from_label.grid(row=1, column=1, ipadx=10)
        self.to_label.grid(row=3, column=1, ipadx=10)
        self.entry.grid(row=1, column=3, ipadx=10)
        self.currency_from.grid(row=1, column=2, ipadx=10)
        self.currency_to.grid(row=3, column=2, ipadx=10)
        self.convert_button.grid(row=2, column=3, ipadx=10)
        self.output_label.grid(row=3, column=3, ipadx=10)
        self.reset_button.grid(row=4, column=3, ipadx=10)


    def convert(self):
        connection = http.client.HTTPSConnection("currency-exchange.p.rapidapi.com")

        api_key = "insert your API key here"
        api_host = "currency-exchange.p.rapidapi.com"
        headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': api_host
        }

        connection.request("GET", f"/exchange?to={self.output_currency.get()}&from={self.input_currency.get()}&q={self.entry.get()}",
                           headers=headers)

        res = connection.getresponse()
        data = res.read()
        self.output_value.set(float(self.entry.get()) * float(data.decode("utf-8")))
        print(data.decode("utf-8"))


    def reset(self):
        self.entry.delete(0, "end")
        self.output_value.set("Converted currency amount will appear here")

def main():
    root = tk.Tk()
    root.geometry("450x150")
    root.title("Currency Converter!")
    root.configure(background="light blue")
    currency_app = Application(master=root)

    currency_app.mainloop()


if __name__ == "__main__":
    main()