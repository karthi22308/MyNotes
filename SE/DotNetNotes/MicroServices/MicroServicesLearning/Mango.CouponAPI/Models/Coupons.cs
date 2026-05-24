using System.ComponentModel.DataAnnotations;

namespace Mango.CouponAPI.Models
{
    public class Coupons
    {
        [Key]
        public int couponid { get; set; }
        [Required]
        public string couponcode { get; set; }
        public double discountamount { get; set; }
        public string description { get; set; }

    }
}
