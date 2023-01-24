// Multi-select handler
$("#subject-select").multiselect({
  includeSelectAllOption: true,
  numberDisplayed: 5,
  onChange: function (option, checked, select) {
    var csub = $(option).val();
    if (checked == true) {
      if (subs.indexOf(csub) < 0) subs.push(csub);
    } else {
      var idx = subs.indexOf(csub);
      if (idx >= 0) subs.splice(idx, 1);
      // In case a conf with multiple types (including this type) is wrongly hid, show all confs with at least one checked type.
      for (var i = 0; i < subs.length; i++) {
        // $('.' + subs[i] + '-conf').show();
      }
    }
    update_filtering({
      subs: subs,
      all_subs: all_subs,
      rankings: rankings,
      all_rankings: all_rankings,
    });
  },
  onSelectAll: function (options) {
    subs = all_subs;
    update_filtering({
      subs: subs,
      all_subs: all_subs,
      rankings: rankings,
      all_rankings: all_rankings,
    });
  },
  onDeselectAll: function (options) {
    subs = [];
    update_filtering({
      subs: subs,
      all_subs: all_subs,
      rankings: rankings,
      all_rankings: all_rankings,
    });
  },
  buttonText: function (options, select) {
    if (options.length === 0) {
      return "None selected";
    } else {
      var labels = [];
      options.each(function () {
        if ($(this).attr("value") !== undefined) {
          labels.push($(this).attr("value"));
        } else {
          labels.push($(this).html());
        }
      });
      return labels.join(", ") + "";
    }
  },
  buttonTitle: function (options, select) {
    return "";
  },
});
$("#ranking-select").multiselect({
  includeSelectAllOption: true,
  numberDisplayed: 5,
  onChange: function (option, checked, select) {
    var cranking = $(option).val();
    if (checked == true) {
      $("." + cranking + "-ranking").show();
      if (rankings.indexOf(cranking) < 0) rankings.push(cranking);
    } else {
      $("." + cranking + "-ranking").hide();
      var idx = rankings.indexOf(cranking);
      if (idx >= 0) rankings.splice(idx, 1);
    }
    update_filtering({
      subs: subs,
      all_subs: all_subs,
      rankings: rankings,
      all_rankings: all_rankings,
    });
  },
  onSelectAll: function (options) {
    rankings = all_rankings;
    update_filtering({
      subs: subs,
      all_subs: all_subs,
      rankings: rankings,
      all_rankings: all_rankings,
    });
  },
  onDeselectAll: function (options) {
    rankings = [];
    update_filtering({
      subs: subs,
      all_subs: all_subs,
      rankings: rankings,
      all_rankings: all_rankings,
    });
  },
  buttonText: function (options, select) {
    if (options.length === 0) {
      return "None selected";
    } else {
      var labels = [];
      options.each(function () {
        if ($(this).attr("value") !== undefined) {
          labels.push($(this).attr("label"));
        } else {
          labels.push($(this).html());
        }
      });
      return labels.join(", ") + "";
    }
  },
  buttonTitle: function (options, select) {
    return "";
  },
});
