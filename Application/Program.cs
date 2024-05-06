using System.Net;
using System.Text;
using System.Text.Json;
using Microsoft.VisualBasic;
using Spectre.Console;

namespace ApaluchaApplication{
    class Program{
        public static string apaluchaAsciiArt = $@"[green3]
    ___                __           __             ___   ____ ___  __ __
   /   |  ____  ____ _/ /_  _______/ /_  ____ _   |__ \ / __ \__ \/ // /
  / /| | / __ \/ __ `/ / / / / ___/ __ \/ __ `/   __/ // / / /_/ / // /_
 / ___ |/ /_/ / /_/ / / /_/ / /__/ / / / /_/ /   / __// /_/ / __/__  __/
/_/  |_/ .___/\__,_/_/\__,_/\___/_/ /_/\__,_/   /____/\____/____/ /_/   
      /_/               
[/]
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
                    AnsiConsole.Markup("\n[white on red]An error occured while getting token. Maybe misspelled URL?[/]\n");
                    return "False";
                }
                else{
                    AnsiConsole.Markup("\n[white on red]An error occured while getting token. Maybe misspelled URL?[/]\n");
                    return "False";
                }
            }
            else{
                Clear(false);
                AnsiConsole.Markup($"[white on red]An error occured while getting token. Maybe misspelled URL?[/][red]\nError:\n[/] {response.ToString()}\n");
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
                    AnsiConsole.Markup($"[white on red]An error occured while parsing response: {e} \nResponse: {responseString}[/]\n");
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
                    AnsiConsole.Markup($"[white on red]An error occured while parsing response: {e} \nResponse: {responseString}[/]\n");
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
                    AnsiConsole.Markup($"[white on red]An error occured while parsing response: {e} \nResponse: {responseString}[/]\n");
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
                            AnsiConsole.Markup($"[white on red]Can't find pdfUrl in response: {responseString}[/]\n");
                            return "500";
                        }
                        return pdfUrl;
                    }
                    catch(Exception e){
                        AnsiConsole.Markup($"[white on red]An error occured while parsing response: {e} \nResponse: {responseString}[/]\n");
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
                    AnsiConsole.Markup($"[white on red]An error occured while parsing response: {e} \nResponse: {responseString}[/]\n");
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
                    AnsiConsole.Markup($"[white on red]An error occured while parsing response: {e} \nResponse: {responseString}[/]\n");
                    return "False";
                }
            }
        }      
        public static async Task<string> ChangeSettings(HttpClient managmentClient, string url, Dictionary<string, dynamic> settings){
            var settingsData = new {
                action = "change_settings",
                data = settings
            };

            string jsonData = JsonSerializer.Serialize(settingsData);
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
                    Console.WriteLine(e);
                    Console.WriteLine(responseString);
                    AnsiConsole.Markup($"[white on red]An error occured while parsing response: {e}\n");
                    return "False";
                }
            }
        }
        public static List<string> OnStartUp(){

            List<string> result = new List<string>();

            string? apiUrl;
            string? username;
            string? password;

            string apiQuestion = "[bold]Enter URL address of the website API[/] (example: https://apalucha.kaktusgame.eu/api): ";
            string usernameQuestion = "[bold]Enter username of admin[/] (Example: admin): ";
            string passwordQuestion = "[bold]Enter password of admin account[/] (Example: admin): ";

            Console.Clear();
            AnsiConsole.Markup(apaluchaAsciiArt);

            AnsiConsole.Markup(apiQuestion);
            apiUrl = Console.ReadLine();
            while(true){
                bool uriTest = Uri.TryCreate(apiUrl, UriKind.Absolute, out Uri? urlResult);
                if(uriTest != false && apiUrl != null){
                    break;
                }
                AnsiConsole.Markup("[white on red]Invalid URL, please try again![/]\n\n");
                AnsiConsole.Markup(apiQuestion);
                apiUrl = Console.ReadLine();
            }

            AnsiConsole.Markup(usernameQuestion);
            username = Console.ReadLine();

            while(string.IsNullOrEmpty(username)){
                AnsiConsole.Markup("[white on red]Please enter some username![/]\n\n");
                AnsiConsole.Markup(usernameQuestion);
                username = Console.ReadLine();
            }

            AnsiConsole.Markup(passwordQuestion);
            password = "";
            ConsoleKeyInfo key = Console.ReadKey(true);
            while (key.Key != ConsoleKey.Enter){
                if (key.Key != ConsoleKey.Backspace){
                    password += key.KeyChar;
                    Console.Write("*");
                }
                else{
                    if (password.Length > 0){
                        password = password.Substring(0, password.Length - 1);
                        Console.Write("\b \b");
                    }
                }
                key = Console.ReadKey(true);
            }

            result.Add(apiUrl);
            result.Add(username);
            result.Add(password);

            return result;
        }
        public static async Task ConsoleAddFilm(HttpClient managmentClient, string url){
            string? title;
            string? team;

            string titleQuestion = "[bold]Enter title of film: [/]";
            string teamQuestion = "[bold]Enter team of film: [/]";

            AnsiConsole.Markup(titleQuestion);
            title = Console.ReadLine();

            while(string.IsNullOrEmpty(title)){
                AnsiConsole.Markup("[white on red]Please enter some title![/]\n\n");
                AnsiConsole.Markup(titleQuestion);
                title = Console.ReadLine();
            }

            AnsiConsole.Markup(teamQuestion);
            team = Console.ReadLine();

            while(string.IsNullOrEmpty(team)){
                AnsiConsole.Markup("[white on red]Please enter some team![/]\n\n");
                AnsiConsole.Markup(teamQuestion);
                team = Console.ReadLine();
            }

            string result = await AddFilm(managmentClient, url, title, team);

            if(result == "True"){
                AnsiConsole.Markup($"[green]Film {title} was added successfully![/]\n\n");
                return;
            }
            else{
                AnsiConsole.Markup($"[white on red]There was an error while adding film {title}: {result}[/]\n\n");
                return;
            }
        }
        public static async Task ConsoleRemoveFilm(HttpClient managmentClient, string url){
            string? title;

            string titleQuestion = "[bold]Enter title of film to remove: [/]";

            AnsiConsole.Markup(titleQuestion);
            title = Console.ReadLine();

            while(string.IsNullOrEmpty(title)){
                AnsiConsole.Markup("[white on red]Please enter some title![/]\n\n");
                AnsiConsole.Markup(titleQuestion);
                title = Console.ReadLine();
            }

            string result = await RemoveFilm(managmentClient, url, title);

            if(result == "True"){
                AnsiConsole.Markup($"[green]Film {title} was removed successfully![/]\n\n");
                return;
            }
            else{
                AnsiConsole.Markup($"[white on red]There was an error while removing film {title}: {result}[/]\n\n");
                return;
            }
        }
        public static async Task ConsoleRemoveUser(HttpClient managmentClient, string url){
            string? username;
            string? isAdminString;
            bool isAdmin;

            string usernameQuestion = "[bold]Enter username of user to remove: [/]";
            string isAdminQuestion = "[bold]Is user admin? (yes/no): [/]";

            AnsiConsole.Markup(usernameQuestion);
            username = Console.ReadLine();

            while(string.IsNullOrEmpty(username)){
                AnsiConsole.Markup("[white on red]Please enter some username![/]\n\n");
                AnsiConsole.Markup(usernameQuestion);
                username = Console.ReadLine();
            }

            AnsiConsole.Markup(isAdminQuestion);
            isAdminString = Console.ReadLine();

            while(string.IsNullOrEmpty(isAdminString)){
                AnsiConsole.Markup("[white on red]Please enter some answer![/]\n\n");
                AnsiConsole.Markup(isAdminQuestion);
                isAdminString = Console.ReadLine();
            }

            if(isAdminString.ToLower() == "yes"){
                isAdmin = true;
            }
            else if(isAdminString.ToLower() == "no"){
                isAdmin = false;
            }
            else{
                AnsiConsole.Markup("[white on red]Invalid answer, please try again![/]\n\n");
                return;
            }

            string result = await RemoveUser(managmentClient, isAdmin, url, username);

            if(result == "True"){
                AnsiConsole.Markup($"[green]User {username} was removed successfully![/]\n\n");
                return;
            }
            else{
                AnsiConsole.Markup($"[white on red]There was an error while removing user {username}: {result}[/]\n\n");
                return;
            }
        }
        public static async Task ConsoleAddUser(HttpClient managementClient, string url){
            string? username;
            string? password;
            string? isAdminString;
            bool isAdmin;

            string usernameQuestion = "[bold]Enter username of user to add: [/]";
            string passwordQuestion = "[bold]Enter password of user to add: [/]";
            string isAdminQuestion = "[bold]Is user admin? (yes/no): [/]";

            AnsiConsole.Markup(isAdminQuestion);
            isAdminString = Console.ReadLine();

            while(string.IsNullOrEmpty(isAdminString)){
                AnsiConsole.Markup("[white on red]Please enter some answer![/]\n\n");
                AnsiConsole.Markup(isAdminQuestion);
                isAdminString = Console.ReadLine();
            }

            if(isAdminString.ToLower() == "yes"){
                isAdmin = true;
            }
            else if(isAdminString.ToLower() == "no"){
                isAdmin = false;
            }
            else{
                AnsiConsole.Markup("[white on red]Invalid answer, please try again![/]\n\n");
                return;
            }

            if(isAdmin == false){
                string pdfUrl = await AddUser(managementClient, isAdmin, url);
                if(pdfUrl == "500"){
                    AnsiConsole.Markup("[white on red]There was an error while adding user![/]\n\n");
                    return;
                }
                else{
                    AnsiConsole.Markup($"[green]User was added successfully![/]\n[bold]PDF URL: [/]{pdfUrl}\n\n");
                    return;
                }
            }
            else{
                AnsiConsole.Markup(usernameQuestion);
                username = Console.ReadLine();

                while(string.IsNullOrEmpty(username)){
                    AnsiConsole.Markup("[white on red]Please enter some username![/]\n\n");
                    AnsiConsole.Markup(usernameQuestion);
                    username = Console.ReadLine();
                }

                AnsiConsole.Markup(passwordQuestion);
                password = Console.ReadLine();

                while(string.IsNullOrEmpty(password)){
                    AnsiConsole.Markup("[white on red]Please enter some password![/]\n\n");
                    AnsiConsole.Markup(passwordQuestion);
                    password = Console.ReadLine();
                }

                string result = await AddUser(managementClient, isAdmin, url, username, password);

                if(result == "True"){
                    AnsiConsole.Markup($"[green]User {username} was added successfully![/]\n\n");
                    return;
                }
                else{
                    AnsiConsole.Markup($"[white on red]There was an error while adding user {username}: {result}[/]\n\n");
                    return;
                }
            }
        }
        public static async Task ConsoleReset(HttpClient managementClient, string url){
            string? resetSecretString;
            string? fullResetString;
            bool resetSecret;
            bool fullReset;

            string resetSecretQuestion = "[bold]Do you want to remove all voting users? (yes/no): [/]";
            string warning = "[black on yellow]Warning: This action is irreversible![/]\n";
            string fullResetQuestion = "[bold]Do you want to do full reset? => Remove all films, etc? (yes/no): [/]";

            AnsiConsole.Markup(warning);
            AnsiConsole.Markup(resetSecretQuestion);
            resetSecretString = Console.ReadLine();

            while(string.IsNullOrEmpty(resetSecretString)){
                AnsiConsole.Markup("[white on red]Please enter some answer![/]\n\n");
                AnsiConsole.Markup(resetSecretQuestion);
                resetSecretString = Console.ReadLine();
            }

            if(resetSecretString.ToLower() == "yes"){
                resetSecret = true;
            }
            else if(resetSecretString.ToLower() == "no"){
                resetSecret = false;
            }
            else{
                AnsiConsole.Markup("[white on red]Invalid answer, please try again![/]\n\n");
                return;
            }
            Console.WriteLine();
            AnsiConsole.Markup(warning);
            AnsiConsole.Markup(fullResetQuestion);
            fullResetString = Console.ReadLine();

            while(string.IsNullOrEmpty(fullResetString)){
                AnsiConsole.Markup("[white on red]Please enter some answer![/]\n\n");
                AnsiConsole.Markup(fullResetQuestion);
                fullResetString = Console.ReadLine();
            }

            if(fullResetString.ToLower() == "yes"){
                fullReset = true;
            }
            else if(fullResetString.ToLower() == "no"){
                fullReset = false;
            }
            else{
                AnsiConsole.Markup("[white on red]Invalid answer, please try again![/]\n\n");
                return;
            }

            string result = await Reset(managementClient, url, resetSecret, fullReset);

            if(result == "True"){
                AnsiConsole.Markup($"[green]Voting was reset successfully! (maybe you will have to restart the app)[/]\n\n");
                return;
            }
            else{
                AnsiConsole.Markup($"[white on red]There was an error while resetting the voting: {result}[/]\n\n");
                return;
            }
        }
        public static async Task ConsoleChangeSettings(HttpClient managementClient, string url){
            string settingForChange = $@"[bold]Choose setting you want to change: [/]
    [bold]1.[/] Voting duration
    [bold]2.[/] Pool size
    [bold]3.[/] JWT expiration time
    [bold]4.[/] Debug mode

If you are done, type [bold]c[/] or [bold]continue[/] to continue.
If you want to quit, type [bold]q[/] or [bold]quit[/].
";

            Dictionary<string, dynamic> settings = new Dictionary<string, dynamic>();
            Clear(false);
            AnsiConsole.Markup(settingForChange);
            AnsiConsole.Markup("[bold]Choose number of setting you want to change: [/]");
            string? setting = Console.ReadLine();
            while(true){
                if(string.IsNullOrEmpty(setting)){
                    AnsiConsole.Markup("[white on red]Please enter some setting![/]\n");
                    setting = Console.ReadLine();
                }
                else{
                    if(setting == "1"){
                        AnsiConsole.Markup("[bold]Enter new voting duration (in seconds -> just number): [/]");
                        string? duration = Console.ReadLine();
                        while(true){
                            if(string.IsNullOrEmpty(duration)){
                                AnsiConsole.Markup("[white on red]Please enter some duration![/]\n");
                            }
                            // check if duration is number
                            else if(!int.TryParse(duration, out int vote_result)){
                                AnsiConsole.Markup("[white on red]Duration must be a number![/]\n");
                            }
                            else{
                                settings.Add("voteDuration", vote_result);
                                break;
                            }
                            AnsiConsole.Markup("[bold]Enter new voting duration (in seconds -> just number): [/]");
                            duration = Console.ReadLine();
                        }
                    }
                    else if(setting == "2"){
                        AnsiConsole.Markup("[bold]Enter new pool size: [/]");
                        string? poolSize = Console.ReadLine();
                        while(true){
                            if(string.IsNullOrEmpty(poolSize)){
                                AnsiConsole.Markup("[white on red]Please enter some pool size![/]\n");
                            }
                            // check if poolSize is number
                            else if(!int.TryParse(poolSize, out int pool_result)){
                                AnsiConsole.Markup("[white on red]Pool size must be a number![/]\n");
                            }
                            else{
                                settings.Add("poolSize", pool_result);
                                break;
                            }
                            AnsiConsole.Markup("[bold]Enter new pool size: [/]");
                            poolSize = Console.ReadLine();
                        }
                    }
                    else if (setting == "3"){
                        AnsiConsole.Markup("[bold]Enter new JWT expiration time (in days -> just number): [/]");
                        string? jwtExpiration = Console.ReadLine();
                        while(true){
                            if(string.IsNullOrEmpty(jwtExpiration)){
                                AnsiConsole.Markup("[white on red]Please enter some JWT expiration time![/]\n");
                            }
                            // check if jwtExpiration is number
                            else if(!int.TryParse(jwtExpiration, out int jwt_result)){
                                AnsiConsole.Markup("[white on red]JWT expiration time must be a number![/]\n");
                            }
                            else{
                                settings.Add("jwtExpiration", jwt_result);
                                break;
                            }
                            AnsiConsole.Markup("[bold]Enter new JWT expiration time (in days -> just number): [/]");
                            jwtExpiration = Console.ReadLine();
                        }
                    }
                    else if (setting == "4"){
                        AnsiConsole.Markup("[bold]Enter new debug mode (true/false): [/]");
                        string? debugMode = Console.ReadLine();
                        while(true){
                            if(string.IsNullOrEmpty(debugMode)){
                                AnsiConsole.Markup("[white on red]Please enter some debug mode![/]\n");
                            }
                            // check if debugMode is boolean
                            else if(!bool.TryParse(debugMode, out bool debug_result)){
                                AnsiConsole.Markup("[white on red]Debug mode must be a boolean![/]\n");
                            }
                            else{
                                settings.Add("debugMode", debug_result);
                                break;
                            }
                            AnsiConsole.Markup("[bold]Enter new debug mode (true/false): [/]");
                            debugMode = Console.ReadLine();
                        }
                    }
                    else if(setting == "q" || setting == "quit"){
                        return;
                    }
                    else if(setting == "c" || setting == "continue"){
                        break;
                    }
                    else{
                        AnsiConsole.Markup("[white on red]Invalid setting, please try again![/]\n");
                        setting = Console.ReadLine();
                    }
                Clear(false);
                AnsiConsole.Markup(settingForChange);
                AnsiConsole.Markup("[bold]Choose number of setting you want to change: [/]");
                setting = Console.ReadLine();
                }
        }
            AnsiConsole.Markup("[bold]These settings will be changed: [/]\n");
            foreach (KeyValuePair<string, dynamic> change in settings){
                AnsiConsole.Markup($"   [bold]{change.Key}[/]: {change.Value}\n");
            }
            AnsiConsole.Markup("[black on yellow]WARNING: Changing settings will lead to server restart! Please be sure that no one is using the app! (it might be down for a while)[/]\n");
            AnsiConsole.Markup("[bold]Do you want to continue? (yes/no): [/]");
            string? continueChange = Console.ReadLine();
            if(continueChange == "no"){
                return;
            }
            else if(continueChange != "yes"){
                AnsiConsole.Markup("[white on red]Invalid answer, please try again![/]\n");
                return;
            }

            string result = await ChangeSettings(managementClient, url, settings);

            if(result == "True"){
                AnsiConsole.Markup($"[green]Settings were changed successfully! (maybe you will have to restart the app)[/]\n\n");
                return;
            }
            else{
                AnsiConsole.Markup($"[white on red]There was an error while changing settings: {result}[/]\n\n");
                return;
            }
        }
        public static void Help(){
            AnsiConsole.Markup("[bold]Available commands:[/]\n");
            AnsiConsole.Markup("[bold]add_film[/] => Add film to the voting\n");
            AnsiConsole.Markup("[bold]remove_film[/] => Remove film from the voting\n");
            AnsiConsole.Markup("[bold]add_user[/] => Add user to the voting\n");
            AnsiConsole.Markup("[bold]remove_user[/] => Remove user from the voting\n");
            AnsiConsole.Markup("[bold]change_settings[/] => Change settings of the voting\n");
            AnsiConsole.Markup("[bold]reset[/] => Reset the voting\n");
            AnsiConsole.Markup("[bold]help[/] => Show available commands\n");
            AnsiConsole.Markup("[bold]clear[/] => Clear the console\n");
            AnsiConsole.Markup("[bold]exit[/] => Exit the app\n");
            Console.WriteLine();
        }
        public static void Clear(bool printHelp=true){
            Console.Clear();
            AnsiConsole.Markup(apaluchaAsciiArt);
            Console.WriteLine();
            if (printHelp){
                AnsiConsole.Markup("[bold]If you need help, type 'help' to see available commands![/]\n");
            }
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
                AnsiConsole.Markup("[bold]Apalucha 2024 >> [/]");
                string? command = Console.ReadLine();
                if(string.IsNullOrEmpty(command)){
                    AnsiConsole.Markup("[white on red]Please enter some command![/]\n");
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
                else if(command == "change_settings"){
                    Clear();
                    await ConsoleChangeSettings(apaluchaClient, apiUrl);
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
                    AnsiConsole.Markup("[white on red]Invalid command, please try again![/]\n");
                }
            }
        }
    }
}