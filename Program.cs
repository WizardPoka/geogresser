// Program.cs

namespace ConsoleApp1
{
    using System;
    using OpenQA.Selenium;
    using OpenQA.Selenium.Chrome;
    using OpenQA.Selenium.Support.UI;
    using System.Threading;
    using OpenQA.Selenium.Interactions;

    internal class Program
    {
        static void Main(string[] args)
        {
            string mail = "palhamberg@gmail.com";
            string pass = "Ispilkeren73";
            // Инициализация драйвера браузера
            IWebDriver driver = new ChromeDriver();
            driver.Navigate().GoToUrl("https://www.geoguessr.com/signin/");

            // Находим поле для ввода электронной почты
            IWebElement emailField = driver.FindElement(By.Name("email"));

            // Вводим текст в поле электронной почты
            emailField.SendKeys(mail);
            emailField.SendKeys(Keys.Tab);

            // Находим поле для ввода пароля
            IWebElement passwordField = driver.FindElement(By.Name("password"));

            // Вводим текст в поле пароля
            passwordField.SendKeys(pass);
            emailField.SendKeys(Keys.Enter);

            Thread.Sleep(500);
            while (true)
            {
                string mapurl = Console.ReadLine();
                mapurl += "/play";
                driver.Navigate().GoToUrl(mapurl);

                Thread.Sleep(500);

                IWebElement challengeButton = driver.FindElement(By.XPath("//img[@alt='Challenge']"));

                Actions actions = new Actions(driver);

                actions.MoveToElement(challengeButton).Click().Perform();

                Thread.Sleep(100);

                IWebElement inviteFriendsButton = driver.FindElement(By.XPath("//button[@data-qa='invite-friends-button']"));

                // Выполняем нужные действия с найденной кнопкой
                inviteFriendsButton.Click(); // Например, кликнуть на кнопку

                Thread.Sleep(500);

                IWebElement linkField = driver.FindElement(By.Name("copy-link"));
                string linkValue = linkField.GetAttribute("value");

                Console.WriteLine(linkValue);

            }
        }
    }
}