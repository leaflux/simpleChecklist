// just a bit more javascript to put the template form labels where I want them
$(function() {
  $("#id_name").before("<label class='helptext'>Name (35 char limit):</label>")

  $("#id_note").before("<label class='helptext'>Note (40 char limit):</label>")

  $("#id_date").before("<label class='helptext'>Due Date:</label><br>")

  $("#id_priority").before("<label class='helptext'>Priority:</label><br>")
});
