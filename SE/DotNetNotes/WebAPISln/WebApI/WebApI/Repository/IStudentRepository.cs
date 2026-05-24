using WebApI.Models.Student;

namespace WebApI.Repository
{
    public interface IStudentRepository
    {


        Task<List<Student>> getstudents();
    }
}
