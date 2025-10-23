using Mango.Models;
using Mango.Web.Models;

namespace Mango.Services.IService
{
    public interface IBaseService
    {
        Task<ResponseDto?> SendAsync(Requestdto request);
    }
}
