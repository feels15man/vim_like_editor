# VIM like editor
VIM like text TUI editor on Python.

The implementation is based on the MVC design pattern. MVC is a fundamental pattern that has found application in many technologies.

For the first time, the MVC pattern appeared in the SmallTalk language. The developers had to come up with an architectural solution that would separate the GUI from the business logic, and the business logic from the data. Thus, in the classic version, MVC consists of three parts, which gave it its name. Consider them:
### Model


A model is usually understood as a part containing the functional business logic of an application. The model must be completely independent from the rest of the product. The model layer should not know anything about the design elements and how it will be displayed. A result is achieved that allows you to change the representation of the data, the way it is displayed, without touching the Model itself.
The model has the following features:
• The model is the business logic of the application;
• The model has knowledge about itself and does not know about controllers and views.;
• For some projects, a model is just a data layer (DAO, database, XML file);
• For other projects, a model is a database manager, a set of objects, or just application logic.;
•	
### View

It is the responsibility of the View to display the data received from the Model. However, the view cannot directly affect the model. We can say that the view has read-only access to the data.

The representation has the following features:

• The view implements the display of data that is received from the Model in any way;
• In some cases, the view may have code that implements some business logic.
In my implementation, the Model stores the text and buffers of the entered commands. The View is responsible for rendering the available data using the adapter class for the curses library. The controller reads the input using the adaptes class for the curses ControllerAdapter library. The adapter is divided into the two aforementioned classes Contrller and View Adapter, which hide the functionality of working with the curses library.
My implementation includes observer and state patterns. The observer pattern for the interaction of View and Model. The status pattern for switching the Controller. That is, the Controller interprets the input differently for each state.
	Several tests have been implemented to test the functionality of the program using the pytest library. To initialize them, it was necessary to implement stubs for adapter classes working with curses, as well as a function initializing the necessary setup_environment components. The tests check the insertion mode input and the state change.

 ### Patterns

 MVC pattern for architecture, Observer pattern for event update, State pattern for different modes of input(Normal state, Input state etc)
