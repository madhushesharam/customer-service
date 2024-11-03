Feature: Customer Service API

  Scenario: Get welcome message
    When I send a GET request to "/"
    Then I should receive a 200 status code
    And the response should contain "welcome to customer service"