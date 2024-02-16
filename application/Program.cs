using System.Net;
using System.Text;
using System.Text.Json;

namespace ApaluchaApplication{
    class Program{
        public static string apaluchaAsciiArt = $@"
    ___                __           __             ___   ____ ___  __ __
   /   |  ____  ____ _/ /_  _______/ /_  ____ _   |__ \ / __ \__ \/ // /
  / /| | / __ \/ __ `/ / / / / ___/ __ \/ __ `/   __/ // / / /_/ / // /_
 / ___ |/ /_/ / /_/ / / /_/ / /__/ / / / /_/ /   / __// /_/ / __/__  __/
/_/  |_/ .___/\__,_/_/\__,_/\___/_/ /_/\__,_/   /____/\____/____/ /_/   
      /_/               


            ";

        // API methods
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
                if (response.Headers.TryGetValues("Set-Cookie", out IEnumerable<string>? values)){
                    foreach (string value in values){
                        if (value.StartsWith("token=")){
                            string token = value.Split(';')[0].Split('=')[1];
                            return token;
                        }
                    }
                    Console.WriteLine("An error occured while getting token. Maybe misspelled URL?");
                    return "False";
                }
                else{
                    Console.WriteLine("An error occured while getting token. Maybe misspelled URL?");
                    return "False";
                }
            }
            else{
                Console.WriteLine($"An error occured while getting token. Maybe misspelled URL?\nError: {response.StatusCode}");
                return "False";
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
                try{
                    var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                    string? message = responseJson.GetProperty("error").GetString();
                    return message ?? "False";
                }
                catch(Exception e){
                    Console.WriteLine($"An error occured while parsing response: {e} \nResponse: {responseString}");
                    return "False";
                }
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
                try{
                    var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                    string? message = responseJson.GetProperty("error").GetString();
                    return message ?? "False";
                }
                catch(Exception e){
                    Console.WriteLine($"An error occured while parsing response: {e} \nResponse: {responseString}");
                    return "False";
                }
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
                try{ 
                    var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                    string? message = responseJson.GetProperty("error").GetString();
                    return message ?? "False";
                }
                catch(Exception e){
                    Console.WriteLine($"An error occured while parsing response: {e} \nResponse: {responseString}");
                    return "False";
                }
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
                    try{
                        var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                        string? pdfUrl = responseJson.GetProperty("pdfUrl").GetString();
                        if(pdfUrl == null){
                            Console.WriteLine("Error: pdfUrl not found in response");
                            return "500";
                        }
                        return pdfUrl;
                    }
                    catch(Exception e){
                        Console.WriteLine($"An error occured while parsing response: {e} \nResponse: {responseString}");
                        return "500";
                    }
                }
                return "True";   
            }
            else{
                string responseString = await result.Content.ReadAsStringAsync();
                try{ 
                    var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                    string? message = responseJson.GetProperty("error").GetString();
                    return message ?? "False";
                }
                catch(Exception e){
                    Console.WriteLine($"An error occured while parsing response: {e} \nResponse: {responseString}");
                    return "False";
                }
            }
        }
        public static async Task<string> Reset(HttpClient managmentClient, string url, bool resetSecret=false, bool fullReset=false){
            var resetData = new {
                action = "reset",
                data = new{
                    reset_secret = resetSecret,
                    full_reset = fullReset
                }
            };

            string jsonData = JsonSerializer.Serialize(resetData);
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            HttpResponseMessage result = await managmentClient.PostAsync(url, content);

            if(result.IsSuccessStatusCode){
                return "True";   
            }
            else{
                string responseString = await result.Content.ReadAsStringAsync();
                try{
                    var responseJson = JsonSerializer.Deserialize<JsonElement>(responseString);
                    string? message = responseJson.GetProperty("error").GetString();
                    return message ?? "False";
                }
                catch(Exception e){
                    Console.WriteLine($"An error occured while parsing response: {e} \nResponse: {responseString}");
                    return "False";
                }
            }
        }
        public static List<string> OnStartUp(){

            List<string> result = new List<string>();

            string? apiUrl;
            string? username;
            string? password;

            string apiQuestion = "Enter URL address of website (Example: https://apalucha.kaktusgame.eu): ";
            string usernameQuestion = "Enter username of admin (Example: admin): ";
            string passwordQuestion = "Enter password of admin account (Example: admin): ";

            Console.Clear();
            Console.WriteLine(apaluchaAsciiArt);

            Console.Write(apiQuestion);
            apiUrl = Console.ReadLine();
            while(true){
                bool uriTest = Uri.TryCreate(apiUrl, UriKind.Absolute, out Uri? urlResult);
                if(uriTest != false && apiUrl != null){
                    break;
                }
                Console.WriteLine("Invalid URL address, please try again!");
                Console.Write(apiQuestion);
                apiUrl = Console.ReadLine();
            }

            Console.Write(usernameQuestion);
            username = Console.ReadLine();

            while(string.IsNullOrEmpty(username)){
                Console.WriteLine("Please enter some username!");
                Console.Write(usernameQuestion);
                username = Console.ReadLine();
            }

            Console.Write(passwordQuestion);
            password = Console.ReadLine();
            while(string.IsNullOrEmpty(password)){
                Console.WriteLine("Please enter some password!");
                Console.Write(passwordQuestion);
                password = Console.ReadLine();
            }

            result.Add(apiUrl);
            result.Add(username);
            result.Add(password);

            return result;
        }
        public static async Task ConsoleAddFilm(HttpClient managmentClient, string url){
            string? title;
            string? team;

            string titleQuestion = "Enter title of film: ";
            string teamQuestion = "Enter team of film: ";

            Console.Write(titleQuestion);
            title = Console.ReadLine();

            while(string.IsNullOrEmpty(title)){
                Console.WriteLine("Please enter some title!");
                Console.Write(titleQuestion);
                title = Console.ReadLine();
            }

            Console.Write(teamQuestion);
            team = Console.ReadLine();

            while(string.IsNullOrEmpty(team)){
                Console.WriteLine("Please enter some team!");
                Console.Write(teamQuestion);
                team = Console.ReadLine();
            }

            string result = await AddFilm(managmentClient, url, title, team);

            if(result == "True"){
                Console.WriteLine($"Film {title} was added successfully!");
                return;
            }
            else{
                Console.WriteLine($"There was an error while adding film {title}: {result}");
                return;
            }
        }
        public static async Task ConsoleRemoveFilm(HttpClient managmentClient, string url){
            string? title;

            string titleQuestion = "Enter title of film to remove: ";

            Console.Write(titleQuestion);
            title = Console.ReadLine();

            while(string.IsNullOrEmpty(title)){
                Console.WriteLine("Please enter some title!");
                Console.Write(titleQuestion);
                title = Console.ReadLine();
            }

            string result = await RemoveFilm(managmentClient, url, title);

            if(result == "True"){
                Console.WriteLine($"Film {title} was removed successfully!");
                return;
            }
            else{
                Console.WriteLine($"There was an error while removing film {title}: {result}");
                return;
            }
        }
        public static async Task ConsoleRemoveUser(HttpClient managmentClient, string url){
            string? username;
            string? isAdminString;
            bool isAdmin;

            string usernameQuestion = "Enter username of user to remove: ";
            string isAdminQuestion = "Is user admin? (yes/no): ";

            Console.Write(usernameQuestion);
            username = Console.ReadLine();

            while(string.IsNullOrEmpty(username)){
                Console.WriteLine("Please enter some username!");
                Console.Write(usernameQuestion);
                username = Console.ReadLine();
            }

            Console.Write(isAdminQuestion);
            isAdminString = Console.ReadLine();

            while(string.IsNullOrEmpty(isAdminString)){
                Console.WriteLine("Please enter some answer!");
                Console.Write(isAdminQuestion);
                isAdminString = Console.ReadLine();
            }

            if(isAdminString.ToLower() == "yes"){
                isAdmin = true;
            }
            else if(isAdminString.ToLower() == "no"){
                isAdmin = false;
            }
            else{
                Console.WriteLine("Invalid answer, please try again!");
                return;
            }

            string result = await RemoveUser(managmentClient, isAdmin, url, username);

            if(result == "True"){
                Console.WriteLine($"User {username} was removed successfully!");
                return;
            }
            else{
                Console.WriteLine($"There was an error while removing user {username}: {result}");
                return;
            }
        }
        public static async Task ConsoleAddUser(HttpClient managementClient, string url){
            string? username;
            string? password;
            string? isAdminString;
            bool isAdmin;

            string usernameQuestion = "Enter username of user to add: ";
            string passwordQuestion = "Enter password of user to add: ";
            string isAdminQuestion = "Is user admin? (yes/no): ";

            Console.Write(isAdminQuestion);
            isAdminString = Console.ReadLine();

            while(string.IsNullOrEmpty(isAdminString)){
                Console.WriteLine("Please enter some answer!");
                Console.Write(isAdminQuestion);
                isAdminString = Console.ReadLine();
            }

            if(isAdminString.ToLower() == "yes"){
                isAdmin = true;
            }
            else if(isAdminString.ToLower() == "no"){
                isAdmin = false;
            }
            else{
                Console.WriteLine("Invalid answer, please try again!");
                return;
            }

            if(isAdmin == false){
                string pdfUrl = await AddUser(managementClient, isAdmin, url);
                if(pdfUrl == "500"){
                    Console.WriteLine("There was an error while adding user!");
                    return;
                }
                Console.WriteLine($"User was added successfully! PDF with QR code is available at: {pdfUrl}");
            }
            else{
                Console.Write(usernameQuestion);
                username = Console.ReadLine();

                while(string.IsNullOrEmpty(username)){
                    Console.WriteLine("Please enter some username!");
                    Console.Write(usernameQuestion);
                    username = Console.ReadLine();
                }

                Console.Write(passwordQuestion);
                password = Console.ReadLine();

                while(string.IsNullOrEmpty(password)){
                    Console.WriteLine("Please enter some password!");
                    Console.Write(passwordQuestion);
                    password = Console.ReadLine();
                }

                string result = await AddUser(managementClient, isAdmin, url, username, password);

                if(result == "True"){
                    Console.WriteLine($"User {username} was added successfully!");
                    return;
                }
                else{
                    Console.WriteLine($"There was an error while adding user {username}: {result}");
                    return;
                }
            }
        }
        public static async Task ConsoleReset(HttpClient managementClient, string url){
            string? resetSecretString;
            string? fullResetString;
            bool resetSecret;
            bool fullReset;

            string resetSecretQuestion = "Do you want to remove all voting users? (yes/no): ";
            string fullResetQuestion = "Do you want to do full reset? => Remove all films, etc? (yes/no): ";

            Console.Write(resetSecretQuestion);
            resetSecretString = Console.ReadLine();

            while(string.IsNullOrEmpty(resetSecretString)){
                Console.WriteLine("Please enter some answer!");
                Console.Write(resetSecretQuestion);
                resetSecretString = Console.ReadLine();
            }

            if(resetSecretString.ToLower() == "yes"){
                resetSecret = true;
            }
            else if(resetSecretString.ToLower() == "no"){
                resetSecret = false;
            }
            else{
                Console.WriteLine("Invalid answer, please try again!");
                return;
            }

            Console.Write(fullResetQuestion);
            fullResetString = Console.ReadLine();

            while(string.IsNullOrEmpty(fullResetString)){
                Console.WriteLine("Please enter some answer!");
                Console.Write(fullResetQuestion);
                fullResetString = Console.ReadLine();
            }

            if(fullResetString.ToLower() == "yes"){
                fullReset = true;
            }
            else if(fullResetString.ToLower() == "no"){
                fullReset = false;
            }
            else{
                Console.WriteLine("Invalid answer, please try again!");
                return;
            }

            string result = await Reset(managementClient, url, resetSecret, fullReset);

            if(result == "True"){
                Console.WriteLine("Reset was successful!");
                return;
            }
            else{
                Console.WriteLine($"There was an error while resetting: {result}");
                return;
            }
        }
        public static void Help(){
            Console.WriteLine("Available commands:");
            Console.WriteLine("add_film - Adds film to database");
            Console.WriteLine("remove_film - Removes film from database");
            Console.WriteLine("add_user - Adds user to database");
            Console.WriteLine("remove_user - Removes user from database");
            Console.WriteLine("help - Shows this message");
            Console.WriteLine("clear - Clears console");
            Console.WriteLine("reset - Resets the voting");
            Console.WriteLine("exit - Exits application");
        }
        public static void Clear(){
            Console.Clear();
            Console.WriteLine(apaluchaAsciiArt);
            Console.WriteLine();
            Console.WriteLine("If you are stuck, type 'help' to see available commands!");
            Console.WriteLine();
        }
        public static async Task Main(){
            List<string> start = OnStartUp();

            string apiUrl = start[0];
            string username = start[1];
            string password = start[2];
            string token = await Login(username, password, apiUrl);

            // Checks if token has token or error code
            if(token == "500" || token == "False"){
                return;
            }

            HttpClientHandler apaluchaHandler = new HttpClientHandler();
            CookieContainer cookieContainer = new CookieContainer();
            HttpClient apaluchaClient = new HttpClient(apaluchaHandler);

            cookieContainer.Add(new Uri(apiUrl), new Cookie("token", token));
            apaluchaHandler.CookieContainer = cookieContainer;
            apiUrl = apiUrl + "/managment";

            Clear();
            while(true){
                Console.Write("Apalucha 2024 >>");
                string? command = Console.ReadLine();
                if(string.IsNullOrEmpty(command)){
                    Console.WriteLine("Invalid command, type 'help' to see available commands!");
                    continue;
                }
                else{
                    command = command.ToLower();
                }
                if(command == "add_film"){
                    Clear();
                    await ConsoleAddFilm(apaluchaClient, apiUrl);
                }
                else if(command == "remove_film"){
                    Clear();
                    await ConsoleRemoveFilm(apaluchaClient, apiUrl);
                }
                else if(command == "add_user"){
                    Clear();
                    await ConsoleAddUser(apaluchaClient, apiUrl);
                }
                else if(command == "remove_user"){
                    Clear();
                    await ConsoleRemoveUser(apaluchaClient, apiUrl);
                }
                else if(command == "reset"){
                    Clear();
                    await ConsoleReset(apaluchaClient, apiUrl);
                }
                else if(command == "help"){
                    Help();
                }
                else if(command == "clear"){
                    Clear();
                }
                else if(command == "exit"){
                    break;
                }
                else{
                    Console.WriteLine("Invalid command, type 'help' to see available commands!");
                }
            }
        }
    }
}