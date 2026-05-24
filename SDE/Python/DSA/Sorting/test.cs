using System;
using System.Collections.Generic;

public class HelloWorld
{
    public static void Main(string[] args)
    {
        List<Student> at = new List<Student> {
            new Student { rollnumber = 1, name = "Karthi" },
            new Student { rollnumber = 2, name = "Arun" }
        };

        at.Add(new Student { rollnumber = 3, name = "Vijay" });
        Console.WriteLine("Try programiz.pro");

    }
}

public class Student
{
    public int rollnumber;
    public string name;
}
