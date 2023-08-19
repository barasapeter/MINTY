using System;

class Calculator {
    static void Main() {
        Console.WriteLine("Simple Calculator\n");

        while (true) {
            Console.Write("Enter the first number: ");
            double num1 = Convert.ToDouble(Console.ReadLine());

            Console.Write("Enter an operator (+, -, *, /): ");
            char op = Convert.ToChar(Console.ReadLine());

            Console.Write("Enter the second number: ");
            double num2 = Convert.ToDouble(Console.ReadLine());

            double result = 0.0;

            switch (op) {
                case '+':
                    result = num1 + num2;
                    break;
                case '-':
                    result = num1 - num2;
                    break;
                case '*':
                    result = num1 * num2;
                    break;
                case '/':
                    if (num2 != 0)
                        result = num1 / num2;
                    else {
                        Console.WriteLine("Error: Cannot divide by zero.");
                        continue; // Restart the loop
                    }
                    break;
                default:
                    Console.WriteLine("Invalid operator.");
                    continue; // Restart the loop
            }

            Console.WriteLine($"Result: {result}\n");

            Console.Write("Do you want to perform another calculation? (Y/N): ");
            char choice = Convert.ToChar(Console.ReadLine());
            if (char.ToUpper(choice) != 'Y')
                break;
        }

        Console.WriteLine("Calculator closed.");
    }
}

