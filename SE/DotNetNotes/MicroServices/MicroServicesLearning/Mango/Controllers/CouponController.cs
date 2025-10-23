using Mango.CouponAPI.Models;
using Mango.Services.IService;
using Mango.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace Mango.Controllers
{
    public class CouponController : Controller
    {
        private readonly ICouponService couponService;
        public CouponController(ICouponService couponService)
        {
            this.couponService = couponService;

        }
        public async Task< IActionResult> CouponIndex()

        {
            List<Coupons>? list = new();
            ResponseDto? res = await couponService.getallcouponsasync();
            if (res != null && res.IsSuccess) { 
                list = JsonConvert.DeserializeObject<List<Coupons>>(Convert.ToString(res.Result));
            }
            return View(list);
        }
    }
}
