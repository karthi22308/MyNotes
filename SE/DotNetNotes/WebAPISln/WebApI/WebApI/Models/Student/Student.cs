namespace WebApI.Models.Student
{
    public class Student
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public string regno { get; set; }
        public Guid stateid { get; set; }

        //nav prop
        public State State { get; set; }
    }
}
