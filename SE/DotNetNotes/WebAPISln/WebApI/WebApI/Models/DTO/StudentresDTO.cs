using WebApI.Models.Student;

namespace WebApI.Models.DTO
{
    public class StudentresDTO
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public string regno { get; set; }
        public Guid stateid { get; set; }
        public string role { get; set; }
    }
}
