# Task App Service

## Usage

All responses will have the form

```json
{
  "data": "Mixed type holding the content of the response"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all tasks

**Definitions**

`GET /api/tasks/`

**Response**

- `200 OK` on success

```json
[
  {
    "id": 1,
    "name": "Do something",
    "status": false,
    "category_id": 1
  },
  {
    "id": 2, 
    "name": "Do another thing", 
    "status": false,
    "category_id": 1 
  }
]
```

### Registering a new task

**Definition**

`POST /api/tasks/`

**Arguments**

- `"name": string` the name of the task (required)
- `"status": boolean` the status of the task (completed/uncompleted), by default is false (uncompleted)
- `"category_id": int` the id of the category (required)

**Response**

- `201 Created` on success

```json
{
  "id": 1,
  "name": "Do something",
  "status": false,
  "category_id": 1
}
```


## Lookup task details

`GET /api/tasks/<id>/`

**Response**

- `404 Not found` if the task does not exist
- `200 OK` on success

```json
{
  "id": 1,
  "name": "Do something",
  "status": false,
  "category_id": 1
}
```

## Delete a task

**Definition**

`DELETE /api/tasks/<id>/`

**Response**

- `404 Not Found` if the task does not exist
- `204 No Content` 


## List all categories


**Definitions**

`GET /api/categories/`

**Response**

- `200 OK` on success

```json
[
  {
    "id": 1,
    "name": "Example category"
  },
  {
    "id": 2, 
    "name": "Another example category"
  }
]
```

### Registering a new category

**Definition**

`POST /api/categories/`

**Arguments**

- `"name": string` the name of the category

**Response**

- `201 Created` on success

```json
{
  "id": 1,
  "name": "Example category"
}
```

## Lookup category details

`GET /api/categories/<id>/`

**Response**

- `404 Not found` if the category does not exist
- `200 OK` on success

```json
{
  "id": 1,
  "name": "Example category"
}
```

## Delete a category

**Definition**

`DELETE /api/categories/<id>/`

**Response**

- `404 Not Found` if the category does not exist
- `204 No Content` 