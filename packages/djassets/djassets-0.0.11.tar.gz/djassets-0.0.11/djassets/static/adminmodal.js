
AdminModal = function (params) {

    var $target = params.$target,
        selector = params.selector,
        onSuccess = params.onSuccess,
        onModalRender = params.onModalRender,
        url = params.url || $target.data('url');

    function afterShow (instance, current) {

        var $modalDoc = $(current.$iframe[0].contentWindow.document),
            $response = $modalDoc.find('#django-admin-popup-response-constants');

        instance.current.$content.height('100%');

        if (!$response.length) {
            if (onModalRender) {
                onModalRender(instance, $modalDoc);
            }
            return;
        }

        if (onSuccess) {
            onSuccess($response.data().popupResponse);
        }

        $.fancybox.destroy();
    }

    function showModal() {
        $.fancybox.open({
            src: url,
            type: 'iframe',
            fitToView: false,
            iframe: {
                preload: false,
            },
            opts: {
                afterShow: afterShow
            }
        });
    }

    if ($target) {
        $target.click(showModal);
    }

    if (selector) {
        $('document').on('click', selector, showModal);
    }

    this.show = showModal;

};
