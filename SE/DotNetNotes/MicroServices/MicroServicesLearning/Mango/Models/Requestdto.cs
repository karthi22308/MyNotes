using static Mango.Models.Constants;

namespace Mango.Models
{
    public class Requestdto
    {
        public ApiType apitype { get; set; } = ApiType.GET;
        public string url { get; set; }
        public object Data { get; set; }
        public string AccessToken { get; set; }

    }
    
}
