using Mango.CouponAPI.Models;
using Microsoft.EntityFrameworkCore;

namespace Mango.CouponAPI.Data
{
    public class appDbcontext : DbContext
    {
        public appDbcontext(DbContextOptions<appDbcontext> options) : base(options)
        {
        }
        public DbSet<Coupons> Coupons { get; set; }
    }
}
