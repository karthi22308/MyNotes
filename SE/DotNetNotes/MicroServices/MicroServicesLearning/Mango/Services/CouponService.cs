using Mango.Models;
using Mango.Services.IService;
using Mango.Web.Models;

namespace Mango.Services
{
    public class CouponService : ICouponService
    {
        private readonly IBaseService baseService;
        public CouponService(IBaseService baseService)
        {
            this.baseService = baseService;
        }
        public async Task<ResponseDto?> getallcouponsasync()
        {
            return await baseService.SendAsync(new Requestdto()
            {
                apitype = Constants.ApiType.GET,
                url = Constants.CouponAPIBase+ "/api/Coupon/GetCoupons"
            });

        }
    }
}
