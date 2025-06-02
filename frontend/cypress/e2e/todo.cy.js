describe('R8UC1: Create To-Do Item', () => {
    let uid;
    let name;
    let email;

    before(function () {
        cy.fixture('user.json').then((user) => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
        }).then((response) => {
            uid = response.body._id.$oid;
            name = user.firstName + ' ' + user.lastName;
            email = user.email;
        });
        });
    });

    beforeEach(function () {
        cy.visit('http://localhost:3000');

        cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email);

        cy.get('form').submit();

        cy.get('h1').should('contain.text', 'Your tasks, ' + name);
    });

    //----R8UC1----
    
    it('R8UC1-TC1: Should create a new to-do', () => {
        cy.get('input[placeholder="Title of your Task"]').type('Cypress Testing', { force: true });
        cy.get('input[placeholder*="watch?v="]').type('dQw4w9WgXcQ', { force: true });
        cy.contains('Create new Task').click({ force: true });

        cy.contains('Cypress Testing').click({ force: true });

        cy.get('input[placeholder="Add a new todo item"]').type('Buy groceries', { force: true });
        cy.contains('Add').click({ force: true });

        cy.contains('Buy groceries').should('exist');
    });

    it('R8UC1-TC2: Should add todo item and add it to the bottom of the list', () => {
        cy.get('input[placeholder="Title of your Task"]').type('Cypress Testing', { force: true });
        cy.get('input[placeholder*="watch?v="]').type('dQw4w9WgXcQ', { force: true });
        cy.contains('Create new Task').click({ force: true });

        cy.contains('Cypress Testing').click({ force: true });

        cy.get('input[placeholder="Add a new todo item"]').type('Help with homework', { force: true });
        cy.contains('Add').click({ force: true });

        cy.get('.todo-item').last().should('contain.text', 'Help with homework');
    });

    it('R8UC1-TC3: Should not add a todo item when input is empty', () => {
        const uniqueTitle = 'Empty Test ' + Date.now();

        cy.get('input[placeholder="Title of your Task"]').type(uniqueTitle, { force: true });
        cy.get('input[placeholder*="watch?v="]').type('dQw4w9WgXcQ', { force: true });
        cy.contains('Create new Task').click({ force: true });

        cy.contains(uniqueTitle).click({ force: true });

        cy.get('input[placeholder="Add a new todo item"]').should('have.value', '');
        cy.contains('Add').click({ force: true });

        cy.get('.task-detail .todo-item').should('have.length', 0);
    });

    //----R8UC2----

    it('R8UC2-TC1: Toggle active to done', () => {
    const uniqueTitle = 'Toggle Test ' + Date.now();
    cy.get('input[placeholder="Title of your Task"]').type(uniqueTitle, { force: true });
    cy.get('input[placeholder*="watch?v="]').type('dQw4w9WgXcQ', { force: true });
    cy.contains('Create new Task').click({ force: true });
    cy.contains(uniqueTitle).click({ force: true });

    cy.get('input[placeholder="Add a new todo item"]').type('Check checkbox', { force: true });
    cy.contains('Add').click({ force: true });

    cy.contains('.todo-item', 'Check checkbox')
      .should('exist') 
      .as('targetTodo');

    cy.get('@targetTodo')
      .find('.checker')
      .click({ force: true });

    cy.get('@targetTodo')
  .find('.checker')
  .should('have.class', 'checked');
});




   it('R8UC2-TC2: Toggle done to active', () => {
    const uniqueTitle = 'Toggle Back Test ' + Date.now();
    const todoText = 'Check checkbox';

    cy.get('input[placeholder="Title of your Task"]').type(uniqueTitle, { force: true });
    cy.get('input[placeholder*="watch?v="]').type('dQw4w9WgXcQ', { force: true });
    cy.contains('Create new Task').click({ force: true });
    cy.contains(uniqueTitle).click({ force: true });

    cy.get('input[placeholder="Add a new todo item"]').type(todoText, { force: true });
    cy.contains('Add').click({ force: true });

    cy.contains('.todo-item', todoText)
      .should('exist')
      .as('targetTodo');

    cy.get('@targetTodo')
      .find('.checker')
      .should('have.class', 'unchecked')
      .click({ force: true });

    cy.get('@targetTodo')
      .find('.checker')
      .should('have.class', 'checked')
      .click({ force: true });

    cy.get('@targetTodo')
      .find('.checker')
      .should('have.class', 'unchecked');
});

//----R8UC3----

it('R8UC3-TC1: Delete a todo item', () => {
        const uniqueTitle = 'Delete Test ' + Date.now();
        cy.get('input[placeholder="Title of your Task"]').type(uniqueTitle, { force: true });
        cy.get('input[placeholder*="watch?v="]').type('dQw4w9WgXcQ', { force: true });
        cy.contains('Create new Task').click({ force: true });
        cy.contains(uniqueTitle).click({ force: true });

        cy.get('input[placeholder="Add a new todo item"]').type('Delete me', { force: true });
        cy.contains('Add').click({ force: true });

        cy.contains('.todo-item', 'Delete me').as('targetTodo');

        cy.get('@targetTodo').find('.remover').click({ force: true });

        cy.get('.todo-item').contains('Delete me').should('not.exist');
    });


    after(function () {
        cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
        });
    });
});