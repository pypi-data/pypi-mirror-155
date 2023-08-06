class UiListSortingView:

    highlight_mode = 'cycleRows'
    highlight_mode_rules = {
        'none': {
            'cycler': [],
        },
        'cycleColumns': {
            'direction': 0,
            'cycler': ['success', 'info', 'warning'],
        },
        'cycleRows': {
            'direction': 1,
            'cycler': ['success', 'info', 'warning'],
        },
        'linearRows': {
            'direction': 1,
            'cycler': ['linear-white'],
        }
    }
