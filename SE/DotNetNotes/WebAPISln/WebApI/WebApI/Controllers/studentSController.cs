using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApI.Data;
using WebApI.Models.DTO;
using WebApI.Models.Student;
using WebApI.Repository;
namespace WebApI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    /////////////class to implement asynchronous programming
    public class studentSController : ControllerBase
    {

        /// <summary>
        /// /class 
        /// </summary>
        private readonly StudentDbContext dbcontext;

        public IStudentRepository Repository { get; }

        public studentSController(StudentDbContext dbContext,IStudentRepository repository)
        {
            this.dbcontext = dbContext;
            Repository = repository;
        }
        [HttpGet]
        public async Task<IActionResult> getstudents()
        {
            var regions = await Repository.getstudents();
            var output = new List<StudentresDTO>();

            foreach (var region in regions)
            {
                output.Add
                    (new StudentresDTO()
                    {
                        Name = region.Name,
                        Id = region.Id,
                        regno = region.regno,
                        stateid = region.stateid,
                        role = "stupid"
                    });

            }

            return Ok(output);
        }

        //get region by id
        [HttpGet]
        [Route("{id:Guid}")]
        public async  Task<IActionResult> getstudent([FromRoute] Guid id)
        {
            //find only uses primary kety
            var student = await dbcontext.students.FindAsync(id);
            //other way with linq
            student = await dbcontext.students.FirstOrDefaultAsync(x => x.Id == id);
            if (student == null)
            {
                return NotFound();
            }
            return Ok(student);
        }
        //insert
        [HttpPost]
        public async Task<IActionResult> addstudent([FromBody] Addstudent input)
        {
            var state = new Student()
            {
                Name = input.Name,
                regno = input.regno


            };

            await dbcontext.students.AddAsync(state);
            await dbcontext.SaveChangesAsync();
            var studen = new Student()
            {
                Name = state.Name,
                regno = state.regno,
                stateid = state.stateid,
                Id = state.Id
            };
            return CreatedAtAction(nameof(getstudent), new { id = state.Id }, studen);
        }
        //update region
        [HttpPut]
        [Route("{id:Guid}")]
        public async Task<IActionResult> updatestudent([FromRoute] Guid id, [FromBody] Addstudent UPDATEPARAM)
        {

            var dto = await dbcontext.students.FirstOrDefaultAsync(X => X.Id == id);
            if (dto == null) return NotFound();
            dto.Name = UPDATEPARAM.Name;
            dto.regno = UPDATEPARAM.regno;
            await dbcontext.SaveChangesAsync(); return Ok(dto);
        }
        [HttpDelete]
        [Route("{id:Guid}")]
        public async Task<IActionResult> updatestudent([FromRoute] Guid id)
        {

            var dto = await  dbcontext.students.FirstOrDefaultAsync(X => X.Id == id);
            if (dto == null) return NotFound();
            dbcontext.students.Remove(dto);
            await dbcontext.SaveChangesAsync(); return Ok(dto);
        }
    }
}
