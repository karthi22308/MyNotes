// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");



string s = "aacdef";
string output = "";
foreach(char c in s)
{
    if (!output.Contains(c))
    {
        output += c;
    }
}

Console.WriteLine(output);


