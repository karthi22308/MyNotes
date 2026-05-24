using Mango.Web.Models;

namespace Mango.Services.IService
{
    public interface ICouponService
    {
        Task<ResponseDto?> getallcouponsasync();
    }
}
