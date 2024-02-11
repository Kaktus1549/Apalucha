using System.Net;
using System.Text;
using System.Text.Json;

namespace ApaluchaApplication{
    
    
    class Program{
        static async Task<string> Login(string username, string password, string url){
            url = url + "/login";
            
            var loginClient = new HttpClient();
            var loginData = new {
                username = username,
                password = password
            };
            
            string jsonData = JsonSerializer.Serialize(loginData);
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await loginClient.PostAsync(url, content);

            if(response.IsSuccessStatusCode){
                string responseString = await response.Content.ReadAsStringAsync();
                var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                string? token = responseJson.GetProperty("token").GetString();
                if(token == null){
                    Console.WriteLine("Error: Token not found in response");
                    return "500";
                }
                return token;
            }
            else{
                return response.StatusCode.ToString();
            }
        }
        public static async Task<string> AddFilm(HttpClient managmentClient, string url, string title, string team){
            var filmData = new {
                action = "add_film",
                data = new{
                    title = title,
                    team = team
                }
            };

            string jsonData = JsonSerializer.Serialize(filmData);
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            HttpResponseMessage result = await managmentClient.PostAsync(url, content);

            if(result.IsSuccessStatusCode){
                return "True";   
            }
            else{
                string responseString = await result.Content.ReadAsStringAsync();
                Console.WriteLine(result.StatusCode);
                var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                string? message = responseJson.GetProperty("error").GetString();
                return message ?? "False";
            }
        }
        public static async Task<string> RemoveFilm(HttpClient managmentClient, string url, string title){
            var filmData = new {
                action = "remove_film",
                data = new{
                    film_id = title
                }
            };

            string jsonData = JsonSerializer.Serialize(filmData);
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            HttpResponseMessage result = await managmentClient.PostAsync(url, content);

            if(result.IsSuccessStatusCode){
                return "True";   
            }
            else{
                string responseString = await result.Content.ReadAsStringAsync();
                var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                string? message = responseJson.GetProperty("error").GetString();
                return message ?? "False";
            }
        }
        public static async Task<string> RemoveUser(HttpClient managmentClient, bool isAdmin, string url, string username){
            var userData = new {
                action = "remove_user",
                data = new{
                    isAdmin = isAdmin,
                    user_id = username
                }
            };

            string jsonData = JsonSerializer.Serialize(userData);
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            HttpResponseMessage result = await managmentClient.PostAsync(url, content);

            if(result.IsSuccessStatusCode){
                return "True";   
            }
            else{
                string responseString = await result.Content.ReadAsStringAsync();
                var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                string? message = responseJson.GetProperty("error").GetString();
                return message ?? "False";
            }
        }
        public static async Task<string> AddUser(HttpClient managmentClient, bool isAdmin, string url, string? username=null, string? password=null){
            var userData = new {
                action = "add_user",
                data = new{
                    isAdmin = isAdmin,
                    username = username,
                    password = password
                }
            };

            string jsonData = JsonSerializer.Serialize(userData);
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            HttpResponseMessage result = await managmentClient.PostAsync(url, content);

            if(result.IsSuccessStatusCode){
                if(isAdmin == false){
                    // if its not admin, server also returns pdfUrl
                    string responseString = await result.Content.ReadAsStringAsync();
                    var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                    string? pdfUrl = responseJson.GetProperty("pdfUrl").GetString();
                    if(pdfUrl == null){
                        Console.WriteLine("Error: pdfUrl not found in response");
                        return "500";
                    }
                    Console.WriteLine(pdfUrl);
                }
                return "True";   
            }
            else{
                string responseString = await result.Content.ReadAsStringAsync();
                var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                string? message = responseJson.GetProperty("error").GetString();
                return message ?? "False";
            }
        }

        public static async Task Main(){
            string apiUrl = "https://apalucha.kaktusgame.eu/api";
            string username = "test";
            string password = "test";
            string token = await Login(username, password, apiUrl);

            HttpClientHandler apaluchaHandler = new HttpClientHandler();
            CookieContainer cookieContainer = new CookieContainer();
            HttpClient apaluchaClient = new HttpClient(apaluchaHandler);

            cookieContainer.Add(new Uri(apiUrl), new Cookie("token", token));
            apaluchaHandler.CookieContainer = cookieContainer;
            apiUrl = apiUrl + "/managment";
        }
    }
}