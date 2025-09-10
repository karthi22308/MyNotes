using System.Globalization;
using System.Net.NetworkInformation;
using System.Security.Cryptography.X509Certificates;
using System.Text;

namespace Practice
{
    internal class Program
    {
        public static int[,] board;
        public static int q;

        public static void printboard()
        {
            for (int i = 0; i < q; i++)
            {
                for (int j = 0; j < q; j++)
                {
                    Console.Write(board[i, j]);
                }
                Console.WriteLine();
            }

        }
        static bool canplace(int x, int y)
        {



            //check up down
            for (int i = 0; i < x; i++)
            {
                if (board[i, y] == 1) return false;
            }

            //check left diagonal
            for (int i = x - 1, j = y - 1; i >= 0 && j >= 0; i--, j--)
            {
                if (board[i, j] == 1) return false;
            }

            //check right diagonal
            for (int i = x - 1, j = y + 1; i >= 0 && j < q; i--, j++)
            {
                if (board[i, j] == 1) return false;
            }

            return true;

        }

        static bool solvenqueens(int i)
        {
            if (i == q)
            {
                return true;
            }

            for (int j = 0; j < q; j++)
            {
                if (canplace(i, j))
                {
                    board[i, j] = 1;
                    if (solvenqueens(i + 1))
                    {
                        return true;
                    }
                    board[i, j] = 0;

                }
            }
            return false;

        }
        public static void helper1()
        {
            Console.WriteLine("1..");
        }
        public static void helper2()
        {
            Console.WriteLine("2..");
        }
        public static void helper3()
        {
            Console.WriteLine("3..");
        }
        public static void nqueens()
        {
            Console.WriteLine("enter queen count..");

            int n = Convert.ToInt32(Console.ReadLine());
            q = n;
            board = new int[n, n];
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    board[i, j] = 0;
                }
            }
            if (!solvenqueens(0))
            {
                Console.WriteLine("not possible");
            }
            else
            {

                printboard();
            }
        }
        public delegate void MyDelegate();
        static void Main(string[] args)
        {


            string qw = "hello";
            string pq = qw;
            pq = "werr";
            Console.WriteLine (qw);
            learn.printsome();
            //MyDelegate myDelegate = delegate { helper1();helper2();helper3(); };
            //myDelegate();

            string s = "Hello world";
            //var words = s.Split(" ");
            //string output="";
            //for (int i = words.Length - 1; i >= 0; i--) 
            //{
            //    output += words[i] +" ";
            //}

            //Console.WriteLine(output);
            //Dictionary<char, int > map = new Dictionary<char, int>();
            //foreach (char c in s)
            //{
            //    if (map.ContainsKey(c))
            //    {
            //        map[c]++;
            //    }
            //    else
            //    {
            //        map[c] = 1;
            //    }
            //}
            //foreach( var pair in map)
            //{
            //    Console.WriteLine(pair.Key.ToString()+ pair.Value.ToString());


            //}
            //int[] ar = new int[] { 5,1,2,8};
            //Array.Sort(ar);
            //Console.WriteLine(ar[ar.Length-2].ToString());
            reverse();

        }
        public static void reverse()
        {
            String s = Console.ReadLine( );

            int  j = s.Length - 1;
            StringBuilder sb = new StringBuilder();
            while (j >= 0)
            {
                sb.Append( s[j] );
                j--;


            }
            s = sb.ToString();
            Console.WriteLine( s );

        }


    }
}
