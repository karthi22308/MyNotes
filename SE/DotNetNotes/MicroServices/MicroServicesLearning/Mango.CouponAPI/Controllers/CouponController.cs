using Mango.CouponAPI.Data;
using Mango.Services.CouponAPI.Models.Dto;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Mango.CouponAPI.Controllers
{
    [Route("api/coupon")]
    [ApiController]
    public class CouponController : Controller
    {
        appDbcontext applicationDbContext;
        ResponseDto res;
        public CouponController(appDbcontext applicationDbContext)
        {
            this.applicationDbContext = applicationDbContext;
            this.res = new ResponseDto();

        }
        [HttpGet("GetCoupons")]
        public async  Task<IActionResult> GetCoupons()
        {
            var coupons = await  applicationDbContext.Coupons.ToListAsync();
            res.Result = coupons;
            res.IsSuccess = true;
            return Ok(res);
        }
    }
}
