namespace ConsoleApplication
{
    public class vehicle
    {
        private readonly string registrationnumber;

        public vehicle(string registrationnumber)
        {
            this.registrationnumber = registrationnumber;
        }

    }
    public class Car : vehicle 
       
    {

        public Car(string registrationnumber )
            :base( registrationnumber ) 
        {
            
        }
    }

    internal class Program
    {
        static void Main(string[] args)
        {
            //section 2 
            Program.classes();

           


        }
        public static void  classes()
        {
            //params sample
            Console.WriteLine(add(1, 2, 3, 4, 5, 6));
            //out keyword sample

            var input = "123";
            int integ;
            var result = int.TryParse(input, out integ);
            if (result == false)
            {
                Console.WriteLine("conversion failed");
            }
            else
            {
                Console.WriteLine("the number is {0}", integ);
            }
            //indexers
            var cookie = new HttpCookie();
            cookie["name"] = "Mosh";
            Console.WriteLine(cookie["name"]);
        }
        public static int add(params int[] ints)
        {
            var output = 0;
            foreach (int i in ints)
            {
                output += i;
            }
            return output;
        }
    }
}
