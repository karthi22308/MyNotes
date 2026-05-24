using AutoMapper;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using WebApI.Data;
using WebApI.Mappings;
using WebApI.Models.DTO;
using WebApI.Models.Student;

namespace WebApI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class studentController : ControllerBase
    {
        //constructor injection of database db context
        private readonly StudentDbContext dbcontext;

        public IMapper Automapper { get; }

        public studentController(StudentDbContext dbContext, IMapper automapper)
        {
                this.dbcontext = dbContext;
            Automapper = automapper;
        }
        [HttpGet]
        public IActionResult getstudents()
        {
            //Automapper
            //nav props
           var regions =  dbcontext.students.Include("State").ToList();
           var output = Automapper.Map <List<StudentresDTO>>(regions);

            return Ok(output);
        }

        //get region by id
        [HttpGet]
        [Route("{id:Guid}")]
        public IActionResult getstudent([FromRoute]Guid id)
        {
            //find only uses primary kety
            var student = dbcontext.students.Find(id);
            //other way with linq
            student = dbcontext.students.FirstOrDefault(x => x.Id == id);
            if (student == null)
            {
                return NotFound();
            }
            return Ok(student);
        }
        //insert
        [HttpPost]
        public IActionResult addstudent([FromBody] Addstudent input)
        {
            var state = new Student()
            {
                Name=input.Name,
                regno   =input.regno

                
            };
           
            dbcontext.students.Add(state);
            dbcontext.SaveChanges();
            var studen = new Student()
            {
                Name = state.Name,
                regno = state.regno,
                stateid = state.stateid,
                Id = state.Id
            };
            return CreatedAtAction(nameof(getstudent),new {id = state.Id},studen);
        }
        //update region
        [HttpPut]
        [Route("{id:Guid}")]
        public IActionResult updatestudent([FromRoute] Guid id, [FromBody] Addstudent UPDATEPARAM)      
        {
            if (ModelState.IsValid)
            {
                var dto = dbcontext.students.FirstOrDefault(X => X.Id == id);
                if (dto == null) return NotFound();
                dto.Name = UPDATEPARAM.Name;
                dto.regno = UPDATEPARAM.regno;
                dbcontext.SaveChanges(); return Ok(dto);
            }
            else
            {
                return NotFound();
            }
        }
        [HttpDelete]
        [Route("{id:Guid}")]
        public IActionResult updatestudent([FromRoute] Guid id)
        {

            var dto = dbcontext.students.FirstOrDefault(X => X.Id == id);
            if (dto == null) return NotFound();
            dbcontext.students.Remove(dto);
            dbcontext.SaveChanges(); return Ok(dto);
        }
    }
}
