using Microsoft.EntityFrameworkCore;
using WebApI.Data;
using WebApI.Models.Student;

namespace WebApI.Repository
{
    public class SQLRegionRepository : IStudentRepository
    {
        private readonly StudentDbContext DbContext;
        public SQLRegionRepository(StudentDbContext dbContext)
        {
            DbContext = dbContext;
        }

      

        public async  Task<List<Student>> getstudents()
        {
            return await DbContext.students.ToListAsync();
        }
    }
}
