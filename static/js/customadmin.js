window.addEventListener("DOMContentLoaded", function () {
  $(document).ready(function () {
    function initSlugCleaning() {
      // eslint-disable-next-line func-names
      $("#id_slug_fr").on("blur", function () {
        // if a user has just set the slug themselves, don't remove stop words etc, just illegal characters
        $(this).val(cleanForSlug($(this).val(), false));
      });
      $("#id_slug_it").on("blur", function () {
        // if a user has just set the slug themselves, don't remove stop words etc, just illegal characters
        $(this).val(cleanForSlug($(this).val(), false));
      });
      $("#id_slug_de").on("blur", function () {
        // if a user has just set the slug themselves, don't remove stop words etc, just illegal characters
        $(this).val(cleanForSlug($(this).val(), false));
      });
      $("#id_slug_en").on("blur", function () {
        // if a user has just set the slug themselves, don't remove stop words etc, just illegal characters
        $(this).val(cleanForSlug($(this).val(), false));
      });
      $("#id_slug_es").on("blur", function () {
        // if a user has just set the slug themselves, don't remove stop words etc, just illegal characters
        $(this).val(cleanForSlug($(this).val(), false));
      });
    }

    function initSlugAutoPopulate() {
      // ----- it -----
      let slug_it_FollowsTitle = $("#id_slug_it").val() == "" && $("#id_title_it").val() == "";
      // eslint-disable-next-line func-names
      $("#id_title").on("keyup keydown keypress blur", function () {
        if (slug_it_FollowsTitle && $("#id_title_it").val() == "") {
          const slugifiedTitle = cleanForSlug(this.value, true);
          $("#id_slug_it").val(slugifiedTitle);
        }
      });
      $("#id_title_it").on("keyup keydown keypress blur", function () {
        const slugifiedTitle = cleanForSlug(this.value, true);
        $("#id_slug_it").val(slugifiedTitle);
      });
      // ----- END fr -----
      // ----- fr -----
      let slug_fr_FollowsTitle = $("#id_slug_fr").val() == "" && $("#id_title_fr").val() == "";
      // eslint-disable-next-line func-names
      $("#id_title").on("keyup keydown keypress blur", function () {
        if (slug_fr_FollowsTitle && $("#id_title_fr").val() == "") {
          const slugifiedTitle = cleanForSlug(this.value, true);
          $("#id_slug_fr").val(slugifiedTitle);
        }
      });
      $("#id_title_fr").on("keyup keydown keypress blur", function () {
        const slugifiedTitle = cleanForSlug(this.value, true);
        $("#id_slug_fr").val(slugifiedTitle);
      });
      // ----- END fr -----
      // ----- de -----
      let slug_de_FollowsTitle = $("#id_slug_de").val() == "" && $("#id_title_de").val() == "";
      // eslint-disable-next-line func-names
      $("#id_title").on("keyup keydown keypress blur", function () {
        if (slug_de_FollowsTitle && $("#id_title_de").val() == "") {
          const slugifiedTitle = cleanForSlug(this.value, true);
          $("#id_slug_de").val(slugifiedTitle);
        }
      });
      $("#id_title_de").on("keyup keydown keypress blur", function () {
        const slugifiedTitle = cleanForSlug(this.value, true);
        $("#id_slug_de").val(slugifiedTitle);
      });
      // ----- END de -----
      // ----- en -----
      let slug_en_FollowsTitle = $("#id_slug_en").val() == "" && $("#id_title_en").val() == "";
      // eslint-disable-next-line func-names
      $("#id_title").on("keyup keydown keypress blur", function () {
        if (slug_en_FollowsTitle && $("#id_title_en").val() == "") {
          const slugifiedTitle = cleanForSlug(this.value, true);
          $("#id_slug_en").val(slugifiedTitle);
        }
      });
      $("#id_title_en").on("keyup keydown keypress blur", function () {
        const slugifiedTitle = cleanForSlug(this.value, true);
        $("#id_slug_en").val(slugifiedTitle);
      });
      // ----- END en -----
      // ----- es -----
      let slug_es_FollowsTitle = $("#id_slug_es").val() == "" && $("#id_title_es").val() == "";
      // eslint-disable-next-line func-names
      $("#id_title").on("keyup keydown keypress blur", function () {
        if (slug_es_FollowsTitle && $("#id_title_es").val() == "") {
          const slugifiedTitle = cleanForSlug(this.value, true);
          $("#id_slug_es").val(slugifiedTitle);
        }
      });
      $("#id_title_es").on("keyup keydown keypress blur", function () {
        const slugifiedTitle = cleanForSlug(this.value, true);
        $("#id_slug_es").val(slugifiedTitle);
      });
      // ----- END es -----
    }

    if (!$("body").hasClass("page-is-live")) {
      initSlugAutoPopulate();
    }
    initSlugCleaning();
  });
});
