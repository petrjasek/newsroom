
import React from 'react';
import { render, createPortal } from 'react-dom';
import { createStore } from 'redux';
import { Provider } from 'react-redux';

import { gettext } from 'utils';

import ShareItemModal from 'wire/components/ShareItemModal';

const store = createStore((state) => ({

}));

class WireDetailApp extends React.Component {
    constructor(props) {
        super(props);

        this.actions = [
            {
                name: gettext('Share'),
                icon: 'share',
            },
            {
                name: gettext('Print'),
                icon: 'print',
            },
            {
                name: gettext('Copy'),
                icon: 'copy',
            },
            {
                name: gettext('Download'),
                icon: 'download',
            }
        ];
    }

    render() {
        const modalData = {items: ['foo'], users: [{_id: 'john', first_name: 'john', last_name: 'doe'}]};

        const modal = createPortal(
            <ShareItemModal key="modal" data={modalData} />,
            document.getElementById('modals')
        );

        return this.actions.map((action) => (
            <span key={action.name} className="wire-column__preview__icon">
                <i className={`icon--${action.icon}`}></i>
            </span>
        )).concat([modal]);
    }
}

render(
    <Provider store={store}>
        <WireDetailApp />
    </Provider>,
    document.getElementById('wire-actions')
);
