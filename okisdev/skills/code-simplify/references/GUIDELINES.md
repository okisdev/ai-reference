# Code Simplification Guidelines

Best practices and patterns for simplifying code.

## 1. Conditional Simplification

### Flatten Nested Conditionals

```javascript
// Before
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      doSomething();
    }
  }
}

// After
if (!user || !user.isActive || !user.hasPermission) return;
doSomething();
```

### Use Early Returns

```javascript
// Before
function process(data) {
  let result;
  if (data) {
    if (data.valid) {
      result = transform(data);
    } else {
      result = null;
    }
  } else {
    result = null;
  }
  return result;
}

// After
function process(data) {
  if (!data?.valid) return null;
  return transform(data);
}
```

## 2. Loop Simplification

### Use Array Methods

```javascript
// Before
const results = [];
for (let i = 0; i < items.length; i++) {
  if (items[i].active) {
    results.push(items[i].name);
  }
}

// After
const results = items.filter(item => item.active).map(item => item.name);
```

### Avoid Index When Unnecessary

```javascript
// Before
for (let i = 0; i < users.length; i++) {
  console.log(users[i].name);
}

// After
for (const user of users) {
  console.log(user.name);
}
```

## 3. Function Simplification

### Extract Repeated Logic

```javascript
// Before
function saveUser(user) {
  user.updatedAt = new Date();
  user.updatedBy = getCurrentUser();
  db.save(user);
}

function savePost(post) {
  post.updatedAt = new Date();
  post.updatedBy = getCurrentUser();
  db.save(post);
}

// After
function withTimestamp(entity) {
  return { ...entity, updatedAt: new Date(), updatedBy: getCurrentUser() };
}

function saveUser(user) {
  db.save(withTimestamp(user));
}

function savePost(post) {
  db.save(withTimestamp(post));
}
```

### Reduce Parameter Count

```javascript
// Before
function createUser(name, email, age, role, department, manager) { ... }

// After
function createUser({ name, email, age, role, department, manager }) { ... }
```

## 4. Naming Improvements

### Use Descriptive Names

```javascript
// Before
const d = new Date();
const u = getUser();
const fn = (x) => x * 2;

// After
const currentDate = new Date();
const currentUser = getUser();
const double = (value) => value * 2;
```

### Boolean Names Should Read as Questions

```javascript
// Before
const user = true;
const loading = false;

// After
const isLoggedIn = true;
const isLoading = false;
```

## 5. Remove Dead Code

- Unused variables
- Unreachable code after returns
- Commented-out code blocks
- Unused imports
- Empty catch blocks (unless intentional)

## 6. Reduce Complexity

### Simplify Boolean Expressions

```javascript
// Before
if (isValid === true) { ... }
if (items.length > 0) { ... }
return condition ? true : false;

// After
if (isValid) { ... }
if (items.length) { ... }
return condition;
```

### Use Optional Chaining

```javascript
// Before
const name = user && user.profile && user.profile.name;

// After
const name = user?.profile?.name;
```

### Use Nullish Coalescing

```javascript
// Before
const value = input !== null && input !== undefined ? input : defaultValue;

// After
const value = input ?? defaultValue;
```

## 7. Error Handling

### Fail Fast

```javascript
// Before
function processOrder(order) {
  if (order) {
    if (order.items) {
      if (order.items.length > 0) {
        // actual logic
      }
    }
  }
}

// After
function processOrder(order) {
  if (!order?.items?.length) {
    throw new Error('Invalid order');
  }
  // actual logic
}
```

## 8. When NOT to Simplify

- Code that is intentionally verbose for debugging
- Performance-critical sections where clarity trades off with speed
- Code matching external API contracts
- Generated code
- Code in active development by others (avoid merge conflicts)
