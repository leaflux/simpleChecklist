$(function() {
  // the 3 types of buttons in my app are set up here: delete list, delete task, and sort (tasks)

  // the 2 delete buttons send list and task ids to the view, and hide themselves after being clicked
  $('.deleteList').click(function() {
    var listid = $(this).attr("data-listid");
    var listElem = $(this);
    $.get('/simple-checklist/delete_todolist/', {list_id: listid}, function(data){
          $('#lists').html(data);
          listElem.hide();
    });
  });

  $('.deleteTask').click(function() {
    var taskid = $(this).attr("data-taskid");
    var listid = $(this).attr("data-listid");
    var taskElem = $(this);
    $.get('/simple-checklist/delete_task/', {list_id: listid, task_id: taskid}, function(data){
        $('#tasks').html(data);
        taskElem.hide();
    });
  });

  // In the todolist template, each sort button has "sort type" data, which is the data type the button sorts tasks by.
  // That information is then used directly as an argument by order_by() in the sort_tasks view
  $('.sort').click(function() {
    var listid = $(this).attr("data-listid");
    var sorttype = $(this).attr("data-sorttype");
    $.get('/simple-checklist/sort_tasks/', {list_id: listid, sort_type: sorttype}, function(data){
        $('#tasks').html(data);
    });
  });

});
