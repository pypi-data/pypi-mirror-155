/**
 * Does not provide the full abstraction layer, only minimizes the difference between bs3 / bs4 / bs5 API.
 */

import { each } from './lib/underscore-esm.js';
import { propGet, propCall } from './prop.js';
import { AppConf } from './conf.js';
import { elements } from './elements.js';
import { initClient } from './initclient.js';
import { Trans } from './translate.js';
import { TransformTags } from './transformtags.js';

var blockTags = {
    list: [
        {
            enclosureTag: '<ul>',
            enclosureClasses: 'list-group',
            itemTag: '<li>',
            itemClasses: 'condensed list-group-item preformatted',
            localKeyTag: '<div>',
            localKeyClasses: 'label label-info label-gray preformatted br-after',
        },
        {
            enclosureTag: '<ul>',
            enclosureClasses: 'list-group',
            itemTag: '<li>',
            itemClasses: 'condensed list-group-item list-group-item-warning preformatted',
            localKeyTag: '<div>',
            localKeyClasses: 'label label-info label-gray preformatted br-after',
        },
    ],
    badges: [
        {
            enclosureTag: '<div>',
            enclosureClasses: 'well well-condensed well-sm',
            itemTag: '<span>',
            itemClasses: 'badge preformatted',
            localKeyTag: '<div>',
            localKeyClasses: 'label label-info label-white preformatted',
        }
    ]
};

var bsTagDef = {
    classPrefix: 'bg-',
    getTagType: function() {
        if (this.hasAttribute('type')) {
            return this.getAttribute('type');
        } else {
            var tagType = this.tagName.split(/-/)[1].toLowerCase();
            if (tagType === 'type') {
                this.setAttribute('type', 'default');
                return 'default';
            } else {
                return tagType;
            }
        }
    },
    connected: function() {
        this.classList.add(this.classPrefix + this.getTagType());
    },
    attributeChanged: {
        type: function(oldValue, newValue) {
            this.classList.remove(this.classPrefix + oldValue);
            this.classList.add(this.classPrefix + newValue);
        }
    }
};

var badgeTagDef = $.extend({
    classes: ['badge'],
}, bsTagDef, {
    classPrefix: 'badge-',
});

var labelTagDef = $.extend({
    classes: ['label'],
}, bsTagDef, {
    classPrefix: 'label-',
});

var cardTagDef = $.extend({
    classes: ['panel'],
}, bsTagDef, {
    classPrefix: 'panel-',
});

var dismissButtonTagDef = {
    ancestor: HTMLButtonElement,
    extendsTagName: 'button',
    classes: ['close'],
    styles: [
        {'text-decoration': 'none'},
        {'border': 'none'},
        {'opacity': '1'},
        {'background-color': 'transparent'},
    ],
    attrs: {
            'aria-label': 'Close',
    },
    innerHTML: '&times;',
};

elements.newCustomElements(
    {
        ancestor: HTMLFormElement,
        name: 'form-inline',
        extendsTagName: 'form',
        classes: ['navbar-form', 'navbar-left']
    },
    {
        ancestor: HTMLDivElement,
        name: 'form-row',
        extendsTagName: 'div',
        classes: ['row', 'form-group'],
    },
    {
        ancestor: HTMLDivElement,
        name: 'form-group',
        extendsTagName: 'div',
        classes: ['form-group'],
    },
    {
        ancestor: HTMLLabelElement,
        name: 'form-label',
        extendsTagName: 'label',
        classes: ['control-label'],
    },
    $.extend(true, {
        name: 'btn-dismiss'
    }, dismissButtonTagDef),
    $.extend(true, {
        name: 'dismiss-alert',
        attrs: {
            'data-dismiss': 'alert',
        }
    }, dismissButtonTagDef),
    $.extend({name: 'badge-type'}, badgeTagDef),
    $.extend({name: 'badge-default'}, badgeTagDef),
    $.extend({name: 'badge-primary'}, badgeTagDef),
    $.extend({name: 'badge-success'}, badgeTagDef),
    $.extend({name: 'badge-info'}, badgeTagDef),
    $.extend({name: 'badge-warning'}, badgeTagDef),
    $.extend({name: 'badge-danger'}, badgeTagDef),
    $.extend({name: 'badge-secondary'}, badgeTagDef),
    $.extend({name: 'badge-light'}, badgeTagDef),
    $.extend({name: 'badge-dark'}, badgeTagDef),
    $.extend({name: 'label-type'}, labelTagDef),
    $.extend({name: 'label-default'}, labelTagDef),
    $.extend({name: 'label-primary'}, labelTagDef),
    $.extend({name: 'label-success'}, labelTagDef),
    $.extend({name: 'label-info'}, labelTagDef),
    $.extend({name: 'label-warning'}, labelTagDef),
    $.extend({name: 'label-danger'}, labelTagDef),
    $.extend({name: 'label-secondary'}, labelTagDef),
    $.extend({name: 'label-light'}, labelTagDef),
    $.extend({name: 'label-dark'}, labelTagDef)
).newBlockElements(
    $.extend({name: 'card-type'}, cardTagDef),
    $.extend({name: 'card-default'}, cardTagDef),
    $.extend({name: 'card-primary'}, cardTagDef),
    $.extend({name: 'card-success'}, cardTagDef),
    $.extend({name: 'card-info'}, cardTagDef),
    $.extend({name: 'card-warning'}, cardTagDef),
    $.extend({name: 'card-danger'}, cardTagDef),
    $.extend({name: 'card-secondary'}, cardTagDef),
    $.extend({name: 'card-light'}, cardTagDef),
    $.extend({name: 'card-dark'}, cardTagDef),
    {
        name: 'card-group',
        classes: ['panel-group']
    },
    {
        name: 'card-header',
        classes: ['panel-heading']
    },
    {
        name: 'card-body',
        classes: ['panel-body']
    },
    {
        name: 'card-footer',
        classes: ['panel-footer']
    },
    {
        name: 'card-title',
        classes: ['panel-title']
    },
    {
        name: 'navbar-default',
        classes: ['nav', 'navbar', 'navbar-default']
    },
);

void function(TransformTags) {

    TransformTags._init = TransformTags.init;

    TransformTags.init = function() {
        this._init();
        this.addAttrs({
            'bs-data': function(elem, attrName) {
                var attrsToRemove = [attrName];
                for (var i = 0; i < elem.attributes.length; i++) {
                    var name = elem.attributes[i].name;
                    if (name !== attrName) {
                        if (name.substr(0, 3) === 'bs-') {
                            elem.setAttribute(
                                'data-' + name.substr(3), elem.attributes[i].value
                            );
                            // attrsToRemove.push(name);
                        }
                    }
                }
                for (var i = 0; i < attrsToRemove.length; i++) {
                    var name = attrsToRemove[i];
                    elem.removeAttribute(name);
                }
            }
        });
        if (AppConf('compatTransformTags')) {
            this.addTags({
                'CARD-TYPE': TransformTags.bsPanel,
                'CARD-DEFAULT': TransformTags.bsPanel,
                'CARD-PRIMARY': TransformTags.bsPanel,
                'CARD-SUCCESS': TransformTags.bsPanel,
                'CARD-INFO': TransformTags.bsPanel,
                'CARD-WARNING': TransformTags.bsPanel,
                'CARD-DANGER': TransformTags.bsPanel,
                'CARD-SECONDARY': TransformTags.bsPanel,
                'CARD-LIGHT': TransformTags.bsPanel,
                'CARD-DARK': TransformTags.bsPanel,
                'CARD-GROUP': TransformTags.bsPanelGroup,
                'CARD-HEADER': TransformTags.bsPanelHeading,
                'CARD-BODY': TransformTags.bsPanelBody,
                'CARD-FOOTER': TransformTags.bsPanelFooter,
                'CARD-TITLE': TransformTags.bsPanelTitle,
                'NAVBAR-DEFAULT': TransformTags.navbarDefault,
                'FORM-INLINE': TransformTags.formInline,
            });
        }
    };

    TransformTags.bsPanel = function(elem, tagName) {
        if (elem.hasAttribute('type')) {
            var typ = elem.getAttribute('type');
            elem.removeAttribute('type');
        } else {
            var typ = tagName.split(/-/)[1].toLowerCase();
        }
        return this.toTag(elem, 'div', 'panel panel-' + typ);
    };

    TransformTags.bsPanelGroup = function(elem, tagName) {
        return this.toTag(elem, 'div', 'panel-group');
    };

    TransformTags.bsPanelHeading = function(elem, tagName) {
        return this.toTag(elem, 'div', 'panel-heading');
    };

    TransformTags.bsPanelBody = function(elem, tagName) {
        return this.toTag(elem, 'div', 'panel-body');
    };

    TransformTags.bsPanelFooter = function(elem, tagName) {
        return this.toTag(elem, 'div', 'panel-footer');
    };

    TransformTags.bsPanelTitle = function(elem, tagName) {
        return this.toTag(elem, 'div', 'panel-title');
    };

    TransformTags.formInline = function(elem, tagName) {
        return this.toTag(elem, 'form', 'navbar-form navbar-left');
    };

    TransformTags.navbarDefault = function(elem, tagName) {
        return this.toTag(elem, 'nav', 'nav navbar navbar-default');
    };

}(TransformTags.prototype);

var transformTags = new TransformTags();


function UiPopover($elem) {

    this.init($elem);

} void function(UiPopover) {

    UiPopover.propCall = propCall;

    UiPopover.init = function($elem) {
        if ($elem instanceof jQuery) {
            if ($elem.length !== 1) {
                throw new Error("Only single element jQuery collection is supported");
            }
            this.elem = $elem.get(0);
        } else if ($elem instanceof HTMLElement) {
            this.elem = $elem;
        } else {
            this.elem = null;
        }
        this.popover = $(this.elem).data('bs.popover');
    };

    UiPopover.isHTML = function(options) {
        return options.content instanceof HTMLElement || options.content instanceof jQuery;
    };

    UiPopover.create = function(options) {
        if (this.popover) {
            throw new Error('Popover is already created');
        }
        options.placement = propGet(options, 'placement', $(this.elem).data('bsPlacement'));
        if (typeof options.placement === 'undefined') {
            options.placement = 'bottom';
        }
        options.html = propGet(options, 'html', $(this.elem).data('bsHtml'));
        if (typeof options.html === 'undefined') {
            options.html = this.isHTML(options);
            // detect callback function, distinguish from HTMLElement / jQuery "function"
            if (!options.html && typeof options.content === 'function') {
                options.content = options.content.call(this.elem);
                options.html = this.isHTML(options);
            }
        }
        if (typeof options.template === 'string') {
            // Convert universal .bs-popover-body to bs3 .popover-content
            var $template = $.contents(options.template);
            $template.find('.bs-popover-body').removeClass('bs-popover-body').addClass('popover-content');
            options.template = $template.prop('outerHTML');
        }
        $(this.elem).popover(options);
    };

    UiPopover.setContent = function($content) {
        if (this.popover) {
            this.popover.options.content = $content;
        }
    };

    UiPopover.hide = function() {
        this.propCall('popover.hide');
    };

    UiPopover.show = function() {
        this.propCall('popover.show');
    };

    UiPopover.close = function() {
        var evt = $(this.elem).data('trigger');
        if (evt !== undefined) {
            $(this.elem).trigger(evt);
        } else {
            this.hide();
        }
    };

    UiPopover.state = function(state) {
        switch (state) {
        case 'show':
            this.show();
            break;
        case 'hide':
            this.hide();
            break;
        default:
            throw new Error('Unknown popover state: ' + state);
        }
    };

    UiPopover.dispose = function() {
        this.propCall('popover.destroy');
    };

    // Find associated input by [data-popover].
    UiPopover.getRelatedInput = function() {
        $('[name="' + CSS.escape($(this.elem).data('popover')) + ']"')
    };

    // check out
    UiPopover.empty = function() {
        var $tip = this.getTip();
        if ($tip.length > 0) {
            var $content = $tip.find('.popover-content');
            initClient($content, 'dispose');
            $tip.find('.popover-content').empty();
        }
    };

    /**
     * Change properties of Bootstrap popover.
     */
    UiPopover.change = function(opts) {
        if (this.popover) {
            for (var opt in opts) {
                if (opts.hasOwnProperty(opt)) {
                    this.popover.options[opt] = opts[opt];
                }
            }
        }
    };

    /**
     * Bootstrap popover notification.
     * Changes properties of Bootstrap popover, show popover and move window scrollpos to related location hash.
     */
    UiPopover.update = function(opts) {
        this.change(opts);
        this.show();
        window.location.hash = '#' + $(this.elem).prop('name');
    };

    /**
     * Get tip DOM element for selected popover.
     */
    UiPopover.getTip = function() {
        return propGet(this.popover, '$tip', $([]));
    };

    UiPopover.isVisible = function() {
        return this.getTip().filter('.in').length > 0;
    };

}(UiPopover.prototype);


function UiTooltip($elem) {

    this.init($elem);

} void function(UiTooltip) {

    UiTooltip.propCall = propCall;

    UiTooltip.init = function($elem) {
        if ($elem instanceof jQuery) {
            if ($elem.length !== 1) {
                throw new Error("Only single element jQuery collection is supported");
            }
            this.elem = $elem.get(0);
        } else {
            this.elem = $elem;
        }
        this.tooltip = $(this.elem).data('bs.tooltip');
    };

    UiTooltip.create = function(options) {
        if (this.tooltip) {
            throw new Error('Tooltip is already created');
        }
        $(this.elem).tooltip(options);
    };

    UiTooltip.hide = function() {
        this.propCall('tooltip.hide');
    };

    UiTooltip.show = function() {
        this.propCall('tooltip.show');
    };

    UiTooltip.dispose = function() {
        this.propCall('tooltip.destroy');
    };

}(UiTooltip.prototype);


function highlightNav(anchor, highlight) {
    var $li = $(anchor).parent('li');
    if (highlight) {
        $li.addClass('active');
    } else {
        $li.removeClass('active');
    }
};

function getCardTitle($elements) {
    return $elements.find('.panel-title:first');
};

function UiDatetimeWidget() {

} void function(UiDatetimeWidget) {

    UiDatetimeWidget.wrap = function() {
        this.$dateControls.wrap('<div class="input-group date datetimepicker"></div>');
        this.$dateControls.after(
            '<div class="input-group-append input-group-addon pointer"><div class="input-group-text glyphicon glyphicon-calendar"></div></div>'
        );
    };

    UiDatetimeWidget.init = function() {
        if (!this.has()) {
            return;
        }
        this.wrap();
        var formatFix = propGet(this.formatFixes, AppConf('languageCode'));
        // Date field widget.
        var options = {
            pickTime: false,
            language: AppConf('languageCode'),
            icons: {
                date: 'calendar'
            }
        };
        if (formatFix !== undefined) {
            options.format = formatFix.date;
        }
        this.$dateControls.filter('.date-control').datetimepicker(options);
        // Datetime field widget.
        options = {
            language: AppConf('languageCode'),
            icons: {
                date: 'calendar'
            }
        };
        if (formatFix !== undefined) {
            options.format = formatFix.datetime;
        }
        this.$dateControls.filter('.datetime-control').datetimepicker(options);
        // Picker window button help.
        this.$selector.find('.picker-switch').prop('title', Trans('Choose year / decade.'));
        // Icon clicking.
        this.$dateControls.next('.input-group-append').on('click', UiDatetimeWidget.open);
        return this;
    };

    // Does not restore DOM into original state, just prevents memory leaks.
    UiDatetimeWidget.destroy = function() {
        if (!this.has()) {
            return;
        }
        this.$dateControls.next('.input-group-append').off('click', UiDatetimeWidget.open);
        // https://github.com/Eonasdan/bootstrap-datetimepicker/issues/573
        each(this.$selector.find('.datetime-control, .date-control'), function(v) {
            var dtp = $(v).data("DateTimePicker");
            // If $.datetimepicker() was added dynamically as empty_form of inline formset,
            // there is no related instance stored in html5 data.
            if (dtp !== undefined) {
                dtp.widget.remove();
            } else {
                /*
                $(v).datetimepicker({language: AppConf('languageCode')});
                var dtp = $(v).data("DateTimePicker");
                dtp.widget.remove();
                */
            }
        });
    };

}(UiDatetimeWidget.prototype);

var ui = {
    defaultDialogSize: BootstrapDialog.SIZE_NORMAL,
    dialogBlockTags: blockTags.badges,
    // Currently available highlight directions:
    //   0 - do not highlight,
    //   1 - highlight columns,
    //   2 - highlight rows,
    highlightModeRules: [
        {
            'none': {
                direction: null,
                header: '',
                cycler: [],
            }
        },
        {
            'cycleColumns': {
                direction: 0,
                header: 'info',
                cycler: ['warning', ''],
            },
        },
        {
            'cycleRows': {
                direction: 1,
                header: 'info',
                cycler: ['warning', ''],
            },
        },
        {
            'linearRows': {
                direction: 1,
                header: '',
                cycler: ['linear-white'],
            }
        },
    ],
    labelClass: 'label',
    version: 3,
};

export { blockTags, transformTags, highlightNav, getCardTitle, UiPopover, UiTooltip, UiDatetimeWidget, ui };
