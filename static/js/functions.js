$('document').ready(function () {
    $('#dismiss-flash').click(function () {
      $('#flash-message').remove();
    });
});

function goToJobLink(id) {
  window.location.href=`/job/${id}`;
};
