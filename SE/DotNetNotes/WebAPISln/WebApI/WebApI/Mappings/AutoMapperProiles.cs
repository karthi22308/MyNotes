using AutoMapper;
using WebApI.Models.DTO;
using WebApI.Models.Student;

namespace WebApI.Mappings
{
    public class AutoMapperProiles : Profile
    {
        public AutoMapperProiles() { 
            CreateMap<StudentresDTO,Student>().ReverseMap();
        }
    }
}
