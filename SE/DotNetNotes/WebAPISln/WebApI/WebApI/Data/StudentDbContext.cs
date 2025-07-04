using Microsoft.EntityFrameworkCore;
using WebApI.Models.Student;

namespace WebApI.Data
{
    public class StudentDbContext: DbContext
    {
        public StudentDbContext(DbContextOptions dbContextOptions): base (dbContextOptions) 
        {
                
        }

        public DbSet<Student> students { get; set; }
        public DbSet<State> states { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            var students = new List<Student>()
            {
                new Student()
                {
                    Name="ck",
                    regno="tsdtgst",
                    Id=Guid.Parse("c15b1190-6915-4c43-9887-63c24ad71cb3")
                }
            };
            modelBuilder.Entity<Student>().HasData(students);


        }

    }
}
